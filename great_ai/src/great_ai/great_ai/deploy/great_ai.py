import inspect
from functools import lru_cache, partial, wraps
from typing import Any, Callable, Iterable, Optional, Sequence, Type, Union, cast

from fastapi import APIRouter, FastAPI, status
from pydantic import BaseModel, create_model

from great_ai.great_ai.views.cache_statistics import CacheStatistics
from great_ai.utilities.parallel_map import parallel_map

from ..constants import METRICS_PATH
from ..context import get_context
from ..dashboard import create_dash_app
from ..helper import (
    freeze_arguments,
    get_function_metadata_store,
    snake_case_to_text,
    use_http_exceptions,
)
from ..parameters import automatically_decorate_parameters
from ..tracing.tracing_context import TracingContext
from ..views import ApiMetadata, HealthCheckResponse, Trace
from .routes import (
    bootstrap_docs_endpoints,
    bootstrap_feedback_endpoints,
    bootstrap_trace_endpoints,
)


class GreatAI:
    def __init__(self, func: Callable[..., Any]):
        self._func = automatically_decorate_parameters(func)
        get_function_metadata_store(self._func).is_finalised = True
        wraps(func)(self)

        self.app = FastAPI(
            title=self.name,
            version=self.version,
            description=self.documentation
            + f"\n\n Find out more on the [metrics page]({METRICS_PATH}).",
            docs_url=None,
            redoc_url=None,
        )

    @freeze_arguments
    @lru_cache(get_context().prediction_cache_size)
    def __call__(self, *args: Any, **kwargs: Any) -> Trace:
        with TracingContext() as t:
            result = self._func(*args, **kwargs)
            output = t.finalise(output=result)
        return output

    @staticmethod
    def deploy(
        func: Optional[Callable[..., Any]] = None,
        *,
        disable_rest_api: bool = False,
        disable_docs: bool = False,
        disable_metrics: bool = False,
    ) -> Union[Callable[[Callable[..., Any]], "GreatAI"], "GreatAI"]:
        if func is None:
            return cast(
                Callable[..., Any],
                partial(
                    GreatAI.deploy,
                    disable_http=disable_rest_api,
                    disable_docs=disable_docs,
                    disable_metrics=disable_metrics,
                ),
            )

        instance = GreatAI(func)

        if not disable_rest_api:
            instance._bootstrap_rest_api(
                disable_docs=disable_docs, disable_metrics=disable_metrics
            )

        return instance

    def process_batch(
        self,
        batch: Iterable[Any],
        concurrency: Optional[int] = None,
    ) -> Sequence[Trace]:
        if not get_context().tracing_database.is_threadsafe:
            concurrency = 1
            get_context().logger.warning("Concurrency is ignored")

        return parallel_map(self, batch, concurrency=concurrency)

    @property
    def name(self) -> str:
        return snake_case_to_text(self._func.__name__)

    @property
    def version(self) -> str:
        return f"{get_context().version}+{get_function_metadata_store(self._func).model_versions}"

    @property
    def documentation(self) -> str:
        return (
            f"GreatAI wrapper for interacting with the `{self._func.__name__}` function.\n\n"
            + (
                "\n".join(
                    line.strip()
                    for line in (self._func.__doc__ or "").split("\n")
                    if line.strip()
                )
            )
        )

    def _bootstrap_rest_api(self, disable_docs: bool, disable_metrics: bool) -> None:
        self._bootstrap_prediction_endpoints()

        if not disable_docs:
            bootstrap_docs_endpoints(self.app)

        if not disable_metrics:
            dash_app = create_dash_app(self._func.__name__, self.documentation)
            bootstrap_trace_endpoints(self.app, dash_app)

        bootstrap_feedback_endpoints(self.app)

        self._bootstrap_meta_endpoints()

    def _bootstrap_prediction_endpoints(self) -> None:
        router = APIRouter(
            prefix="/predictions",
            tags=["predictions"],
        )

        schema = self._get_schema()

        @router.post("/", status_code=status.HTTP_200_OK, response_model=Trace)
        @use_http_exceptions
        def predict(input_value: schema) -> Trace:  # type: ignore
            return self(**cast(BaseModel, input_value).dict())

        self.app.include_router(router)

    def _get_schema(self) -> Type[BaseModel]:
        signature = inspect.signature(self._func)
        parameters = {
            p.name: (
                p.annotation if p.annotation != inspect._empty else Any,
                p.default if p.default != inspect._empty else ...,
            )
            for p in signature.parameters.values()
            if p.name in get_function_metadata_store(self._func).input_parameter_names
        }

        schema: Type[BaseModel] = create_model("InputModel", **parameters)  # type: ignore
        return schema

    def _bootstrap_meta_endpoints(self) -> None:
        router = APIRouter(
            tags=["meta"],
        )

        @router.get("/health", status_code=status.HTTP_200_OK)
        def check_health() -> HealthCheckResponse:
            hits, misses, maxsize, cache_size = self.__call__.cache_info()  # type: ignore
            cache_statistics = CacheStatistics(
                hits=hits, misses=misses, size=cache_size, max_size=maxsize
            )

            return HealthCheckResponse(
                is_healthy=True, cache_statistics=cache_statistics
            )

        @router.get(
            "/version", response_model=ApiMetadata, status_code=status.HTTP_200_OK
        )
        def get_version() -> ApiMetadata:
            return ApiMetadata(
                name=self.name,
                version=self.version,
                documentation=self.documentation,
                configuration=get_context().to_flat_dict(),
            )

        self.app.include_router(router)
