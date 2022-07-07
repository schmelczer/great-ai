from functools import lru_cache, partial, wraps
from textwrap import dedent
from typing import (
    Any,
    Awaitable,
    Callable,
    Generic,
    List,
    Optional,
    Protocol,
    Sequence,
    TypeVar,
    Union,
    cast,
    overload,
)

from async_lru import alru_cache
from fastapi import FastAPI

from ..constants import DASHBOARD_PATH
from ..context import get_context
from ..helper import freeze_arguments, get_function_metadata_store, snake_case_to_text
from ..models import model_versions
from ..parameters import automatically_decorate_parameters
from ..tracing.tracing_context import TracingContext
from ..utilities import parallel_map
from ..views import ApiMetadata, Trace
from .routes.bootstrap_dashboard import bootstrap_dashboard
from .routes.bootstrap_docs_endpoints import bootstrap_docs_endpoints
from .routes.bootstrap_feedback_endpoints import bootstrap_feedback_endpoints
from .routes.bootstrap_meta_endpoints import bootstrap_meta_endpoints
from .routes.bootstrap_prediction_endpoint import bootstrap_prediction_endpoint
from .routes.bootstrap_trace_endpoints import bootstrap_trace_endpoints
from .routes.route_config import RouteConfig

T = TypeVar("T", bound=Union[Trace, Awaitable[Trace]])
V = TypeVar("V")


class GreatAI(Generic[T, V]):
    __name__: str
    __doc__: str

    class FactoryProtocol(Protocol):
        @overload
        def __call__(  # type: ignore
            self,
            func: Callable[..., Awaitable[V]],
        ) -> "GreatAI[Awaitable[Trace[V]], V]":

            ...

        @overload
        def __call__(
            self,
            func: Callable[..., V],
        ) -> "GreatAI[Trace[V], V]":
            ...

    def __init__(
        self,
        func: Callable[..., Union[V, Awaitable[V]]],
        version: Union[str, int],
        route_config: RouteConfig,
    ):
        func = automatically_decorate_parameters(func)
        get_function_metadata_store(func).is_finalised = True

        self._cached_func = self._get_cached_traced_function(func)
        self._wrapped_func = wraps(func)(freeze_arguments(self._cached_func))

        wraps(func)(self)
        self.__doc__ = f"GreatAI wrapper for interacting with the `{self.__name__}` function.\n\n{dedent(self.__doc__ or '')}"

        self.version = str(version)
        flat_model_versions = ".".join(f"{k}-v{v}" for k, v in model_versions)
        if flat_model_versions:
            self.version += f"+{flat_model_versions}"

        self.app = FastAPI(
            title=snake_case_to_text(self.__name__),
            version=self.version,
            description=self.__doc__
            + f"\n\nFind out more in the [dashboard]({DASHBOARD_PATH}).",
            docs_url=None,
            redoc_url=None,
        )

        self._bootstrap_rest_api(route_config)

    @overload
    @staticmethod
    def create(  # type: ignore
        # "Overloaded function signatures 1 and 2 overlap with incompatible return types"
        # https://github.com/python/mypy/issues/12759
        func: Callable[..., Awaitable[V]],
    ) -> "GreatAI[Awaitable[Trace[V]], V]":
        ...

    @overload
    @staticmethod
    def create(
        func: Callable[..., V],
    ) -> "GreatAI[Trace[V], V]":
        ...

    @overload
    @staticmethod
    def create(
        func: None = ...,
        *,
        version: Union[str, int] = ...,
        route_config: RouteConfig = ...,
    ) -> FactoryProtocol:
        ...

    @staticmethod
    def create(
        func: Optional[Callable] = None,
        *,
        version: Union[str, int] = "0.0.1",
        route_config: RouteConfig = RouteConfig(),
    ) -> Union[
        FactoryProtocol, "GreatAI[Awaitable[Trace[V]], V]", "GreatAI[Trace[V], V]"
    ]:
        def factory(_func):  # type: ignore
            return GreatAI[Trace[V], V](
                _func,
                version=version,
                route_config=route_config,
            )

        if func is None:
            return cast(GreatAI.FactoryProtocol, factory)
        else:
            return factory(func)

    def __call__(self, *args: Any, **kwargs: Any) -> T:
        return self._wrapped_func(*args, **kwargs)

    def process_batch(
        self,
        batch: Sequence,
        concurrency: Optional[int] = None,
        do_not_persist_traces: Optional[bool] = False,
    ) -> List[Trace[V]]:
        return list(
            parallel_map(
                partial(
                    self._wrapped_func, do_not_persist_traces=do_not_persist_traces
                ),
                batch,
                concurrency=concurrency,
            )
        )

    @staticmethod
    def _get_cached_traced_function(
        func: Callable[..., Union[V, Awaitable[V]]]
    ) -> Callable[..., T]:
        @lru_cache(maxsize=get_context().prediction_cache_size)
        def func_in_tracing_context_sync(
            *args: Any,
            do_not_persist_traces: bool = False,
            **kwargs: Any,
        ) -> T:
            with TracingContext[V](
                func.__name__, do_not_persist_traces=do_not_persist_traces
            ) as t:
                result = func(*args, **kwargs)
                return cast(T, t.finalise(output=result))

        @alru_cache(maxsize=get_context().prediction_cache_size)
        async def func_in_tracing_context_async(
            *args: Any,
            do_not_persist_traces: bool = False,
            **kwargs: Any,
        ) -> T:
            with TracingContext[V](
                func.__name__, do_not_persist_traces=do_not_persist_traces
            ) as t:
                result = await cast(Callable[..., Awaitable], func)(*args, **kwargs)
                return cast(T, t.finalise(output=result))

        return cast(
            Callable[..., T],
            (
                func_in_tracing_context_async
                if get_function_metadata_store(func).is_asynchronous
                else func_in_tracing_context_sync
            ),
        )

    def _bootstrap_rest_api(self, route_config: RouteConfig) -> None:
        if route_config.prediction_endpoint_enabled:
            bootstrap_prediction_endpoint(self.app, self._wrapped_func)

        if route_config.docs_endpoints_enabled:
            bootstrap_docs_endpoints(self.app)

        if route_config.dashboard_enabled:
            bootstrap_dashboard(
                self.app,
                function_name=self.__name__,
                documentation=self.__doc__,
            )

        if route_config.trace_endpoints_enabled:
            bootstrap_trace_endpoints(self.app)

        if route_config.feedback_endpoints_enabled:
            bootstrap_feedback_endpoints(self.app)

        if route_config.meta_endpoints_enabled:
            bootstrap_meta_endpoints(
                self.app,
                self._cached_func,
                ApiMetadata(
                    name=self.__name__,
                    version=self.version,
                    documentation=self.__doc__,
                    configuration=get_context().to_flat_dict(),
                ),
            )
