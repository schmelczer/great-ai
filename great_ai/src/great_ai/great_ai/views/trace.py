from typing import Any, Dict, Optional

import yaml
from pydantic import validator

from .trace_view import TraceView


class Trace(TraceView):
    models_flat: Optional[str]
    output_flat: Optional[str]
    feedback_flat: Optional[str]

    @validator("models_flat", always=True)
    def flatten_models(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        return ", ".join(f"{m.key}:{m.version}" for m in values["models"])

    @validator("output_flat", always=True)
    def flatten_output(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        return yaml.dump(values["output"], default_flow_style=False, indent=2)

    def to_flat_dict(self) -> Dict[str, Any]:
        return {
            "trace_id": self.trace_id,
            "created": self.created,
            "original_execution_time_ms": self.original_execution_time_ms,
            "models_flat": self.models_flat,
            "output_flat": self.output_flat,
            "exception": self.exception or "null",
            "feedback_flat": self.feedback_flat or "null",
            **self.logged_values,
        }

    def __hash__(self) -> int:
        return hash((type(self),) + tuple(self.__dict__.values()))
