import inspect
from functools import partial
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

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, create_model
from starlette.responses import HTMLResponse

from great_ai.great_ai.helper.use_http_exceptions import use_http_exceptions
from great_ai.utilities.parallel_map import parallel_map

from ..context import get_context
from ..dashboard import create_dash_app
from ..helper import get_function_metadata_store, snake_case_to_text
from ..parameters import automatically_decorate_parameters
from ..tracing import TracingContext
from ..views import EvaluationFeedbackRequest, HealthCheckResponse, Query, Trace

PATH = Path(__file__).parent.resolve()


class GreatAI(FastAPI):
    def __init__(self, func: Callable[..., Any], *args: Any, **kwargs: Any):
        self._func = automatically_decorate_parameters(func)

        schema = self._get_schema()

        def process_single(input_value: schema) -> Trace:  # type: ignore
            with TracingContext() as t:
                result = self._func(**cast(BaseModel, input_value).dict())
                output = t.finalise(output=result)
            return output

        self.process_single = process_single

        super().__init__(
            *args,
            title=snake_case_to_text(func.__name__),
            description=self.documentation,
            docs_url=None,
            version=get_function_metadata_store(func).version,
            redoc_url=None,
            **kwargs,
        )

    @staticmethod
    def deploy(
        func: Optional[Callable[..., Any]] = None,
        *,
        disable_docs: bool = False,
        disable_metrics: bool = False,
    ) -> Union[Callable[[Callable[..., Any]], "GreatAI"], "GreatAI"]:
        if func is None:
            return cast(
                Callable[..., Any],
                partial(
                    GreatAI.deploy,
                    disable_docs=disable_docs,
                    disable_metrics=disable_metrics,
                ),
            )

        return GreatAI(func)._bootstrap_rest_api(
            disable_docs=disable_docs, disable_metrics=disable_metrics
        )

    def process_batch(
        self,
        batch: Iterable[Any],
        concurrency: Optional[int] = None,
    ) -> Sequence[Trace]:
        if not get_context().persistence.is_threadsafe:
            concurrency = 1
            get_context().logger.warning("Concurrency is ignored")

        return parallel_map(self.process_single, batch, concurrency=concurrency)

    @property
    def documentation(self) -> str:
        return (
            f"GreatAI wrapper for interacting with the '{self._func.__name__}' function.\n"
            + (self._func.__doc__ or "")
        )

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

    def _bootstrap_rest_api(
        self, disable_docs: bool, disable_metrics: bool
    ) -> "GreatAI":
        self.post("/evaluations", status_code=status.HTTP_200_OK, response_model=Trace)(
            use_http_exceptions(self.process_single)
        )

        @self.get("/evaluations/:evaluation_id", status_code=status.HTTP_200_OK)
        def get_evaluation(evaluation_id: str) -> Trace:
            result = get_context().persistence.get_trace(evaluation_id)
            if result is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
            return result

        @self.post(
            "/evaluations/:evaluation_id/feedback", status_code=status.HTTP_202_ACCEPTED
        )
        def give_feedback(evaluation_id: str, input: EvaluationFeedbackRequest) -> None:
            get_context().persistence.add_evaluation(evaluation_id, input.evaluation)

        if not disable_docs:

            @self.get("/docs", include_in_schema=False)
            def custom_swagger_ui_html() -> HTMLResponse:
                return get_swagger_ui_html(openapi_url="openapi.json", title=self.title)

            @self.get("/docs/index.html", include_in_schema=False)
            def redirect_to_docs() -> RedirectResponse:
                return RedirectResponse("/docs")

        if not disable_metrics:
            dash_app = create_dash_app(self._func.__name__, self.documentation)
            self.mount(get_context().metrics_path, WSGIMiddleware(dash_app))

            @self.get("/", include_in_schema=False)
            def redirect_to_entrypoint() -> RedirectResponse:
                return RedirectResponse("/metrics")

            self.mount(
                "/assets",
                StaticFiles(directory=PATH / "../dashboard/assets"),
                name="static",
            )

            @self.post("/query", status_code=status.HTTP_200_OK)
            def query_metrics(query: Query) -> List[Dict[str, Any]]:
                return get_context().persistence.query(
                    conjunctive_filters=query.filter,
                    sort_by=query.sort,
                    skip=query.skip,
                    take=query.take,
                )

        @self.get("/health", status_code=status.HTTP_200_OK)
        def check_health() -> HealthCheckResponse:
            return HealthCheckResponse(is_healthy=True)

        return self
