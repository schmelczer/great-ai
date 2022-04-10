from typing import Any, Dict, List

from fastapi import FastAPI, status
from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import RedirectResponse
from starlette.responses import HTMLResponse

from ..context import get_context
from ..helper import snake_case_to_text
from ..metrics import create_dash_app
from ..views import HealthCheckResponse, Query


def create_fastapi_app(
    function_name: str, disable_docs: bool, disable_metrics: bool
) -> FastAPI:
    app = FastAPI(
        title=snake_case_to_text(function_name),
        description=f"REST API wrapper for interacting with the '{function_name}' function.",
        docs_url=None,
        redoc_url=None,
    )

    if not disable_docs:

        @app.get("/docs", include_in_schema=False)
        def custom_swagger_ui_html() -> HTMLResponse:
            return get_swagger_ui_html(openapi_url="openapi.json", title=app.title)

        @app.get("/docs/index.html", include_in_schema=False)
        def redirect_to_entrypoint() -> RedirectResponse:
            return RedirectResponse("/docs")

    if not disable_metrics:
        dash_app = create_dash_app(function_name)
        app.mount(get_context().metrics_path, WSGIMiddleware(dash_app))

        @app.get("/", include_in_schema=False)
        def redirect_to_entrypoint() -> RedirectResponse:
            return RedirectResponse("/metrics")

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
