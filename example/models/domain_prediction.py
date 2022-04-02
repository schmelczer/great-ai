from typing import List

from pydantic import BaseModel


class DomainPrediction(BaseModel):
    domain: str
    probability: float
    explanation: List[str]
