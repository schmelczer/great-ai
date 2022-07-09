from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import RedirectResponse
from starlette.responses import HTMLResponse


def bootstrap_docs_endpoints(app: FastAPI) -> None:
    @app.get("/docs", include_in_schema=False)
    def custom_swagger_ui_html() -> HTMLResponse:
        return get_swagger_ui_html(
            openapi_url="openapi.json",
            title=app.title,
            swagger_favicon_url="/favicon.ico",
        )

    @app.get("/docs/index.html", include_in_schema=False)
    def redirect_to_docs() -> RedirectResponse:
        return RedirectResponse("/docs")
