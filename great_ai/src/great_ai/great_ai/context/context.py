from logging import Logger
from typing import Optional

from pydantic import BaseModel

from ..persistence import PersistenceDriver


class Context(BaseModel):
    version: str
    persistence: PersistenceDriver
    is_production: bool
    logger: Logger
    should_log_exception_stack: bool
    prediction_cache_size: int

    class Config:
        arbitrary_types_allowed = True


_context: Optional[Context] = None
