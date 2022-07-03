from typing import List

from fastapi import APIRouter, FastAPI, HTTPException, Response, status

from ...context import get_context
from ...views import Query, Trace


def bootstrap_trace_endpoints(app: FastAPI) -> None:
    router = APIRouter(
        prefix="/traces",
        tags=["traces"],
    )

    @router.post("", status_code=status.HTTP_200_OK, response_model=List[Trace])
    def query_traces(
        query: Query,
        skip: int = 0,
        take: int = 100,
    ) -> List[Trace]:
        return get_context().tracing_database.query(
            conjunctive_filters=query.filter,
            conjunctive_tags=query.conjunctive_tags,
            since=query.since,
            until=query.until,
            has_feedback=query.has_feedback,
            sort_by=query.sort,
            skip=skip,
            take=take,
        )[0]

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
