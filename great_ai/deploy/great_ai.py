from functools import lru_cache, wraps
from textwrap import dedent
from typing import (
    Any,
    Awaitable,
    Callable,
    Generic,
    List,
    Literal,
    Optional,
    Sequence,
    Tuple,
    TypeVar,
    Union,
    cast,
    overload,
)

from async_lru import alru_cache
from fastapi import FastAPI
from tqdm.cli import tqdm

from ..constants import DASHBOARD_PATH
from ..context import get_context
from ..helper import freeze_arguments, get_function_metadata_store, snake_case_to_text
from ..models.use_model import model_versions
from ..parameters.automatically_decorate_parameters import (
    automatically_decorate_parameters,
)
from ..tracing.tracing_context import TracingContext
from ..utilities import parallel_map
from ..views import ApiMetadata, Trace
from .routes.bootstrap_dashboard import bootstrap_dashboard
from .routes.bootstrap_docs_endpoints import bootstrap_docs_endpoints
from .routes.bootstrap_feedback_endpoints import bootstrap_feedback_endpoints
from .routes.bootstrap_meta_endpoints import bootstrap_meta_endpoints
from .routes.bootstrap_prediction_endpoint import bootstrap_prediction_endpoint
from .routes.bootstrap_trace_endpoints import bootstrap_trace_endpoints

T = TypeVar("T", bound=Union[Trace, Awaitable[Trace]])
V = TypeVar("V")


class GreatAI(Generic[T, V]):
    """Wrapper for a prediction function providing the implementation of SE4ML best practices.

    Provides caching (with argument freezing), a TracingContext during execution, the
    scaffolding of HTTP endpoints using FastAPI and a dashboard using Dash.

    IMPORTANT: when a request is served from cache, no new trace is created. Thus, the
    same trace can be returned multiple times. If this is undesirable turn off caching
    using `configure(prediction_cache_size=0)`.

    Supports wrapping async and synchronous functions while also maintaining correct
    typing.

    Attributes:
        app: FastAPI instance wrapping the scaffolded endpoints and the Dash app.
        version: SemVer derived from the app's version and the model names and versions
            registered through use_model.
    """

    __name__: str  # help for MyPy
    __doc__: str  # help for MyPy

    def __init__(
        self,
        func: Callable[..., Union[V, Awaitable[V]]],
    ):
        """Do not call this function directly, use GreatAI.create instead."""

        func = automatically_decorate_parameters(func)
        get_function_metadata_store(func).is_finalised = True

        self._cached_func = self._get_cached_traced_function(func)
        self._wrapped_func = wraps(func)(freeze_arguments(self._cached_func))

        wraps(func)(self)
        self.__doc__ = (
            f"GreatAI wrapper for interacting with the `{self.__name__}` "
            + f"function.\n\n{dedent(self.__doc__ or '')}"
        )

        self.version = str(get_context().version)
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

        self._bootstrap_rest_api()

    @overload
    @staticmethod
    def create(  # type: ignore
        # Overloaded function signatures 1 and 2 overlap with incompatible return types
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

    @staticmethod
    def create(
        func: Union[Callable[..., Awaitable[V]], Callable[..., V]],
    ) -> Union["GreatAI[Awaitable[Trace[V]], V]", "GreatAI[Trace[V], V]"]:
        """Decorate a function by wrapping it in a GreatAI instance.

        The function can be typed, synchronous or async. If it has
        unwrapped parameters (parameters not affected by a
        [@parameter][great_ai.parameter] or [@use_model][great_ai.use_model] decorator),
        those will be automatically wrapped.

        The return value is replaced by a Trace (or Awaitable[Trace]),
        while the original return value is available under the `.output`
        property.

        For configuration options, see [great_ai.configure][].

        Examples:
            >>> @GreatAI.create
            ... def my_function(a):
            ...     return a + 2
            >>> my_function(3).output
            5

            >>> @GreatAI.create
            ... def my_function(a: int) -> int:
            ...     return a + 2
            >>> my_function(3)
            Trace[int]...

            >>> my_function('3').output
            Traceback (most recent call last):
                ...
            TypeError: type of a must be int; got str instead

        Args:
            func: The prediction function that needs to be decorated.

        Returns:
            A GreatAI instance wrapping `func`.
        """

        return GreatAI[Trace[V], V](
            func,
        )

    def __call__(self, *args: Any, **kwargs: Any) -> T:
        return self._wrapped_func(*args, **kwargs)

    @overload
    def process_batch(
        self,
        batch: Sequence[Tuple],
        *,
        concurrency: Optional[int] = None,
        unpack_arguments: Literal[True],
        do_not_persist_traces: bool = ...,
    ) -> List[Trace[V]]:
        ...

    @overload
    def process_batch(
        self,
        batch: Sequence,
        *,
        concurrency: Optional[int] = None,
        unpack_arguments: Literal[False] = ...,
        do_not_persist_traces: bool = ...,
    ) -> List[Trace[V]]:
        ...

    def process_batch(
        self,
        batch: Sequence,
        *,
        concurrency: Optional[int] = None,
        unpack_arguments: bool = False,
        do_not_persist_traces: bool = False,
    ) -> List[Trace[V]]:
        """Map the wrapped function over a list of input_values (`batch`).

        A wrapper over [parallel_map][great_ai.utilities.parallel_map.parallel_map.parallel_map]
        providing type-safety and a progressbar through tqdm.

        Args:
            batch: A list of arguments for the original (wrapped) function. If the
                function expects multiple arguments, provide a list of tuples and set
                `unpack_arguments=True`.
            concurrency: Number of processes to start. Don't set it too much higher than
                the number of available CPU cores.
            unpack_arguments: Expect a list of tuples and unpack the tuples before
                giving them to the wrapped function.
            do_not_persist_traces: Don't save the traces in the database. Useful for
                evaluations run part of the CI.
        """

        wrapped_function = self._wrapped_func

        def inner(value: Any) -> T:
            return (
                wrapped_function(*value, do_not_persist_traces=do_not_persist_traces)
                if unpack_arguments
                else wrapped_function(
                    value, do_not_persist_traces=do_not_persist_traces
                )
            )

        async def inner_async(value: Any) -> T:
            return await cast(
                Awaitable,
                (
                    wrapped_function(
                        *value, do_not_persist_traces=do_not_persist_traces
                    )
                    if unpack_arguments
                    else wrapped_function(
                        value, do_not_persist_traces=do_not_persist_traces
                    )
                ),
            )

        return list(
            tqdm(
                parallel_map(
                    inner_async
                    if get_function_metadata_store(self).is_asynchronous
                    else inner,
                    batch,
                    concurrency=concurrency,
                ),
                total=len(batch),
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

    def _bootstrap_rest_api(
        self,
    ) -> None:
        route_config = get_context().route_config

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
