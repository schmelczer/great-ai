from typing import Any

from fastapi import APIRouter, FastAPI, HTTPException, Response, status

from ...context import get_context
from ...views import EvaluationFeedbackRequest


def bootstrap_feedback_endpoints(app: FastAPI) -> None:
    router = APIRouter(
        prefix="/traces/{trace_id}/feedback",
        tags=["feedback"],
    )

    @router.put("/", status_code=status.HTTP_202_ACCEPTED)
    def set_feedback(trace_id: str, input: EvaluationFeedbackRequest) -> Response:
        trace = get_context().tracing_database.get(trace_id)
        if trace is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        trace.feedback = input.feedback

        get_context().tracing_database.update(trace_id, trace)
        return Response(status_code=status.HTTP_202_ACCEPTED)

    @router.get("/", status_code=status.HTTP_200_OK)
    def get_feedback(trace_id: str) -> Any:
        trace = get_context().tracing_database.get(trace_id)
        if trace is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return trace.feedback

    @router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
    def delete_feedback(trace_id: str) -> Any:
        trace = get_context().tracing_database.get(trace_id)
        if trace is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        trace.feedback = None

        get_context().tracing_database.update(trace_id, trace)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    app.include_router(router)
