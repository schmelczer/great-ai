from typing import Any

from pydantic import BaseModel


class EvaluationFeedbackRequest(BaseModel):
    feedback: Any
