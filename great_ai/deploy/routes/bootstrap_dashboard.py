from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from ...constants import DASHBOARD_PATH
from .dashboard.create_dash_app import create_dash_app

PATH = Path(__file__).parent.resolve()


def bootstrap_dashboard(app: FastAPI, function_name: str, documentation: str) -> None:
    dash_app = create_dash_app(function_name, app.version, documentation)

    @app.get("/favicon.ico", include_in_schema=False)
    @app.get(f"{DASHBOARD_PATH}/_favicon.ico", include_in_schema=False)
    def get_favicon() -> FileResponse:
        return FileResponse(PATH / "dashboard/assets/favicon.ico")

    app.mount(DASHBOARD_PATH, WSGIMiddleware(dash_app))

    @app.get("/", include_in_schema=False)
    def redirect_to_entrypoint() -> RedirectResponse:
        return RedirectResponse(DASHBOARD_PATH)

    app.mount(
        "/assets",
        StaticFiles(directory=PATH / "dashboard/assets"),
        name="static",
    )
