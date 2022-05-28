import inspect
from functools import lru_cache, partial, wraps
from pathlib import Path
from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    List,
    Optional,
    Sequence,
    Type,
    Union,
    cast,
)

from fastapi import APIRouter, FastAPI, HTTPException, status
from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, create_model
from starlette.responses import HTMLResponse

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
from ..tracing import TracingContext
from ..views import (
    ApiMetadata,
    EvaluationFeedbackRequest,
    HealthCheckResponse,
    Query,
    Trace,
)

PATH = Path(__file__).parent.resolve()


class GreatAI:
    def __init__(self, func: Callable[..., Any]):
        self._func = automatically_decorate_parameters(func)
        self._func = freeze_arguments(
            lru_cache(get_context().prediction_cache_size)(self._func)
        )

        get_function_metadata_store(self._func).is_finalised = True
        wraps(func)(self)

        self.app = FastAPI(
            title=self.name,
            version=self.version,
            description=self.documentation,
            docs_url=None,
            redoc_url=None,
        )

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
        if not get_context().persistence.is_threadsafe:
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
        self._bootstrap_feedback_endpoints()
        self._bootstrap_meta_endpoints()

        if not disable_docs:
            self._bootstrap_docs_endpoints()

        if not disable_metrics:
            self._bootstrap_metrics_endpoints()

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

        @router.get(
            "/:prediction_id", response_model=Trace, status_code=status.HTTP_200_OK
        )
        def get_prediction(prediction_id: str) -> Trace:
            result = get_context().persistence.get_trace(prediction_id)
            if result is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
            return result

        @router.delete("/:prediction_id", status_code=status.HTTP_204_NO_CONTENT)
        def delete_prediction(prediction_id: str) -> None:
            get_context().persistence.delete_trace(prediction_id)

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

    def _bootstrap_feedback_endpoints(self) -> None:
        router = APIRouter(
            prefix="/predictions/:prediction_id/feedback",
            tags=["feedback"],
        )

        @router.put("/", status_code=status.HTTP_202_ACCEPTED)
        def set_feedback(prediction_id: str, input: EvaluationFeedbackRequest) -> None:
            get_context().persistence.add_feedback(prediction_id, input.evaluation)

        @router.get("/", status_code=status.HTTP_200_OK)
        def get_feedback(prediction_id: str) -> Any:
            return get_context().persistence.get_feedback(prediction_id)

        @router.delete("/", status_code=status.HTTP_200_OK)
        def delete_feedback(prediction_id: str) -> Any:
            get_context().persistence.delete_feedback(prediction_id)

        self.app.include_router(router)

    def _bootstrap_meta_endpoints(self) -> None:
        router = APIRouter(
            tags=["meta"],
        )

        @router.get("/health", status_code=status.HTTP_200_OK)
        def check_health() -> HealthCheckResponse:
            return HealthCheckResponse(is_healthy=True)

        @router.get(
            "/version", response_model=ApiMetadata, status_code=status.HTTP_200_OK
        )
        def get_version() -> ApiMetadata:
            return ApiMetadata(
                name=self.name, version=self.version, documentation=self.documentation
            )

        self.app.include_router(router)

    def _bootstrap_docs_endpoints(self) -> None:
        @self.app.get("/docs", include_in_schema=False)
        def custom_swagger_ui_html() -> HTMLResponse:
            return get_swagger_ui_html(openapi_url="openapi.json", title=self.app.title)

        @self.app.get("/docs/index.html", include_in_schema=False)
        def redirect_to_docs() -> RedirectResponse:
            return RedirectResponse("/docs")

    def _bootstrap_metrics_endpoints(self) -> None:
        dash_app = create_dash_app(self._func.__name__, self.documentation)
        self.app.mount(METRICS_PATH, WSGIMiddleware(dash_app))

        @self.app.get("/", include_in_schema=False)
        def redirect_to_entrypoint() -> RedirectResponse:
            return RedirectResponse("/metrics")

        self.app.mount(
            "/assets",
            StaticFiles(directory=PATH / "../dashboard/assets"),
            name="static",
        )

        router = APIRouter(
            prefix="/metrics",
            tags=["metrics"],
        )

        @router.post("/query", status_code=status.HTTP_200_OK)
        def query_metrics(query: Query) -> List[Dict[str, Any]]:
            return get_context().persistence.query(
                conjunctive_filters=query.filter,
                sort_by=query.sort,
                skip=query.skip,
                take=query.take,
            )

        self.app.include_router(router)
