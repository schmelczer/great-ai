from typing import Any, Dict, List, Optional
from uuid import uuid4

from pydantic import BaseModel, validator

from .model import Model


class TraceView(BaseModel):
    trace_id: Optional[str]
    created: str
    original_execution_time_ms: float
    logged_values: Dict[str, Any]
    models: List[Model]
    exception: Optional[str]
    output: Any
    feedback: Any = None

    @validator("trace_id", always=True)
    def generate_id(cls, v: Optional[str], values: Dict[str, Any]) -> Optional[str]:
        if not v:
            return str(uuid4())
        return v

    def __hash__(self) -> int:
        return hash((type(self),) + tuple(self.__dict__.values()))
