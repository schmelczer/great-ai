from pathlib import Path
from typing import Any, Callable, Dict, List

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.responses import HTMLResponse

from ..context import get_context
from ..helper import snake_case_to_text
from ..metrics import create_dash_app
from ..tracing import TracingContext
from ..views import EvaluationFeedbackRequest, HealthCheckResponse, Query, Trace

PATH = Path(__file__).parent.resolve()


def create_service(
    func: Callable[..., Any], disable_docs: bool = False, disable_metrics: bool = False
) -> FastAPI:
    function_name = func.__name__
    function_docs = func.__doc__

    documentation = (
        f"REST API wrapper for interacting with the '{function_name}' function.\n"
    )
    if function_docs:
        documentation += function_docs

    app = FastAPI(
        title=snake_case_to_text(function_name),
        description=documentation,
        docs_url=None,
        redoc_url=None,
    )

    @app.post("/evaluations", status_code=status.HTTP_200_OK, response_model=Trace)
    def score(input: Any) -> Trace:
        with TracingContext() as t:
            result = func(input)
            output = t.log_output(result)
        return output

    @app.get("/evaluations/:evaluation_id", status_code=status.HTTP_200_OK)
    def get_evaluation(evaluation_id: str) -> Trace:
        result = get_context().persistence.get_trace(evaluation_id)
        if result is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return result

    @app.post(
        "/evaluations/:evaluation_id/feedback", status_code=status.HTTP_202_ACCEPTED
    )
    def give_feedback(evaluation_id: str, input: EvaluationFeedbackRequest) -> None:
        get_context().persistence.add_evaluation(evaluation_id, input.evaluation)

    if not disable_docs:

        @app.get("/docs", include_in_schema=False)
        def custom_swagger_ui_html() -> HTMLResponse:
            return get_swagger_ui_html(openapi_url="openapi.json", title=app.title)

        @app.get("/docs/index.html", include_in_schema=False)
        def redirect_to_entrypoint() -> RedirectResponse:
            return RedirectResponse("/docs")

    if not disable_metrics:
        dash_app = create_dash_app(function_name, documentation)
        app.mount(get_context().metrics_path, WSGIMiddleware(dash_app))

        @app.get("/", include_in_schema=False)
        def redirect_to_entrypoint() -> RedirectResponse:
            return RedirectResponse("/metrics")

        app.mount(
            "/assets", StaticFiles(directory=PATH / "../metrics/assets"), name="static"
        )

        @app.post("/query", status_code=status.HTTP_200_OK)
        def query_metrics(query: Query) -> List[Dict[str, Any]]:
            return get_context().persistence.query(
                conjunctive_filters=query.filter,
                sort_by=query.sort,
                skip=query.skip,
                take=query.take,
            )

    @app.get("/health", status_code=status.HTTP_200_OK)
    def check_health() -> HealthCheckResponse:
        return HealthCheckResponse(is_healthy=True)

    return app
