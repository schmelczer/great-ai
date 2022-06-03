from json import dumps
from typing import Any, Dict, List, Optional
from uuid import uuid4

from pydantic import BaseModel, validator

from .model import Model


class Trace(BaseModel):
    trace_id: Optional[str]
    created: str
    execution_time_ms: float
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

    def to_flat_dict(self) -> Dict[str, Any]:
        return {
            "id": self.trace_id,
            "created": self.created,
            "execution_time_ms": self.execution_time_ms,
            "models": ", ".join(f"{m.key}:{m.version}" for m in self.models),
            "output": dumps(self.output),
            "exception": self.exception or "null",
            "feedback": self.feedback,
            **self.logged_values,
        }

    def __hash__(self) -> int:
        return hash((type(self),) + tuple(self.__dict__.values()))
