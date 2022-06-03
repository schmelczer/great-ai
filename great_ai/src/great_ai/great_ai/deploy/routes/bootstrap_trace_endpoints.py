from pathlib import Path
from typing import List

from fastapi import APIRouter, FastAPI, HTTPException, Response, status
from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from flask import Flask

from ...constants import METRICS_PATH
from ...context import get_context
from ...views import Query, Trace

PATH = Path(__file__).parent.resolve()


def bootstrap_trace_endpoints(app: FastAPI, dash_app: Flask) -> None:
    app.mount(METRICS_PATH, WSGIMiddleware(dash_app))

    @app.get("/", include_in_schema=False)
    def redirect_to_entrypoint() -> RedirectResponse:
        return RedirectResponse("/metrics")

    app.mount(
        "/assets",
        StaticFiles(directory=PATH / "../../dashboard/assets"),
        name="static",
    )

    router = APIRouter(
        prefix="/traces",
        tags=["traces"],
    )

    @router.post("/", status_code=status.HTTP_200_OK, response_model=List[Trace])
    def query_traces(
        query: Query,
        skip: int = 0,
        take: int = 100,
    ) -> List[Trace]:
        return get_context().tracing_database.query(
            conjunctive_filters=query.filter,
            sort_by=query.sort,
            skip=skip,
            take=take,
        )

    @router.get("/{trace_id}", status_code=status.HTTP_200_OK, response_model=Trace)
    def get_trace(trace_id: str) -> Trace:
        result = get_context().tracing_database.get(trace_id)
        if result is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return result

    @router.delete("/{trace_id}", status_code=status.HTTP_204_NO_CONTENT)
    def delete_trace(trace_id: str) -> Response:
        get_context().tracing_database.delete(trace_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    app.include_router(router)
