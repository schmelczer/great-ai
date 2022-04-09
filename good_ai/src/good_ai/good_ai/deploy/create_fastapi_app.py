from fastapi import FastAPI, status
from fastapi.openapi.docs import get_swagger_ui_html
from starlette.responses import HTMLResponse

from ..helper import snake_case_to_text
from ..views import HealthCheckResponse


def create_fastapi_app(function_name: str, disable_docs: bool) -> FastAPI:
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

    @app.get("/health", status_code=status.HTTP_200_OK)
    def check_health() -> HealthCheckResponse:
        return HealthCheckResponse(is_healthy=True)

    return app
