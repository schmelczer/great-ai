from typing import Any

from pydantic import BaseModel


class EvaluationFeedbackRequest(BaseModel):
    evaluation: Any
