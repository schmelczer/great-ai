from logging import Logger
from typing import Any, Dict, Optional, Type

from pydantic import BaseModel

from great_ai.large_file.large_file.large_file import LargeFile

from ..tracing.tracing_database import TracingDatabase


class Context(BaseModel):
    tracing_database: TracingDatabase
    large_file_implementation: Type[LargeFile]
    is_production: bool
    logger: Logger
    should_log_exception_stack: bool
    prediction_cache_size: int

    class Config:
        arbitrary_types_allowed = True

    def to_flat_dict(self) -> Dict[str, Any]:
        return {
            "tracing_database": type(self.tracing_database).__name__,
            "large_file_implementation": self.large_file_implementation.__name__,
            "is_production": self.is_production,
            "should_log_exception_stack": self.should_log_exception_stack,
            "prediction_cache_size": self.prediction_cache_size,
        }


_context: Optional[Context] = None
