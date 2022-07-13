from typing import List

from pydantic import BaseModel

from .match import Match


class EvaluatedSentence(BaseModel):
    score: float
    text: str
    explanation: List[Match]
