from typing import Any, Dict, Generic, List, Optional, TypeVar
from uuid import uuid4

import yaml
from pydantic import validator

from ..helper import HashableBaseModel
from .model import Model

T = TypeVar("T")


class Trace(HashableBaseModel, Generic[T]):
    trace_id: Optional[str]
    created: str
    original_execution_time_ms: float
    logged_values: Dict[str, Any]
    models: List[Model]
    exception: Optional[str]
    output: T
    feedback: Any = None
    tags: List[str]

    @validator("trace_id", always=True)
    def generate_id(cls, v: Optional[str], values: Dict[str, Any]) -> Optional[str]:
        if not v:
            return str(uuid4())
        return v

    @property
    def input(self) -> Any:
        return (
            self.logged_values["input"]
            if list(self.logged_values.keys()) == ["input"]
            else self.logged_values
        )

    @property
    def models_flat(self) -> str:
        return ", ".join(f"{m.key}:{m.version}" for m in self.models)

    @property
    def output_flat(self) -> str:
        return yaml.dump(self.output, stream=None)

    @property
    def feedback_flat(self) -> str:
        return (
            "null" if self.feedback is None else yaml.dump(self.feedback, stream=None)
        )

    @property
    def tags_flat(self) -> str:
        return ",\n".join(self.tags)

    def to_flat_dict(self) -> Dict[str, Any]:
        return {
            "trace_id": self.trace_id,
            "created": self.created,
            "original_execution_time_ms": self.original_execution_time_ms,
            **self.logged_values,
            "models_flat": self.models_flat,
            "exception": "null" if self.exception is None else self.exception,
            "output_flat": self.output_flat,
            "feedback_flat": self.feedback_flat,
            "tags_flat": self.tags_flat,
        }
