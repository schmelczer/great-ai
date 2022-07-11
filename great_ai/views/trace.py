from pprint import pformat
from typing import Any, Dict, Generic, List, Optional, TypeVar

from pydantic import Extra

from .hashable_base_model import HashableBaseModel
from .model import Model

T = TypeVar("T")


class Trace(Generic[T], HashableBaseModel):
    trace_id: str
    created: str
    original_execution_time_ms: float
    logged_values: Dict[str, Any]
    models: List[Model]
    exception: Optional[str]
    output: Optional[T]
    feedback: Any = None
    tags: List[str]

    class Config:
        extra = Extra.ignore

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
        return pformat(self.output, indent=2, compact=True)

    @property
    def exception_flat(self) -> str:
        return (
            "null"
            if self.exception is None
            else pformat(self.exception, indent=2, compact=True)
        )

    @property
    def feedback_flat(self) -> str:
        return (
            "null"
            if self.feedback is None
            else pformat(self.feedback, indent=2, compact=True)
        )

    @property
    def tags_flat(self) -> str:
        return ",\n".join(self.tags)

    def to_flat_dict(self, include_original: bool = True) -> Dict[str, Any]:
        return {
            **(
                self.dict()
                if include_original
                else {
                    "trace_id": self.trace_id,
                    "created": self.created,
                    "original_execution_time_ms": self.original_execution_time_ms,
                }
            ),
            **{
                k: pformat(v, indent=2, compact=True)
                for k, v in self.logged_values.items()
            },
            "models_flat": self.models_flat,
            "exception_flat": self.exception_flat,
            "output_flat": self.output_flat,
            "feedback_flat": self.feedback_flat,
            "tags_flat": self.tags_flat,
        }

    def __repr__(self) -> str:
        return f"""Trace[{type(self.output).__name__}]({
            pformat(self.dict(), indent=2, compact=True).replace('{ ', '{', 1)
        })"""
