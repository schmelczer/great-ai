from typing import Any, List

from pydantic import BaseModel

from .model import Model


class Trace(BaseModel):
    created: str
    execution_time_ms: float
    input: Any
    models: List[Model]
    output: Any
    evaluation: Any = None
