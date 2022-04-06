from typing import Any, Callable

import uvicorn
from fastapi import FastAPI, status
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import RedirectResponse
from starlette.responses import HTMLResponse
from typing_extensions import Never

from ..set_default_config import set_default_config_if_uninitialized
from ..tracing import TracingContext
from ..views import HealthCheckResponse, Trace


def serve(
    function: Callable[..., Any],
) -> Never:
    set_default_config_if_uninitialized()

    app = FastAPI(
        title=function.__name__.capitalize().replace("_", " "),
        description=f"REST API wrapper for interacting with the {function.__name__} function.",
        docs_url=None,
        redoc_url=None,
    )

    @app.get("/", include_in_schema=False)
    def redirect_to_docs() -> RedirectResponse:
        return RedirectResponse("/docs")

    @app.get("/docs", include_in_schema=False)
    def custom_swagger_ui_html() -> HTMLResponse:
        return get_swagger_ui_html(openapi_url="openapi.json", title=app.title)

    @app.get("/health", status_code=status.HTTP_200_OK)
    def check_health() -> HealthCheckResponse:
        return HealthCheckResponse(is_healthy=True)

    @app.post("/score", status_code=status.HTTP_200_OK, response_model=Trace)
    def process(input: Any) -> Trace:
        with TracingContext() as t:
            t.log_input(input)
            result = function(input)
            output = t.log_output(result)
        return output

    uvicorn.run(app, host="0.0.0.0", port=5050)
