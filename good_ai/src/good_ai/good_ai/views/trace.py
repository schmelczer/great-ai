from typing import Any, List
from uuid import uuid4

from pydantic import BaseModel

from .model import Model


class Trace(BaseModel):
    id = str(uuid4())
    created: str
    execution_time_ms: float
    input: Any
    models: List[Model]
    output: Any
    evaluation: Any = None
