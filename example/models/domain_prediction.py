from pydantic import BaseModel
from typing import List


class DomainPrediction(BaseModel):
    domain: str
    probability: float
    explanation: List[str]