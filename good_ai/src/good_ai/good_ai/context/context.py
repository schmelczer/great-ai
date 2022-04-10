from logging import Logger

from pydantic import BaseModel

from ..persistence import PersistenceDriver


class Context(BaseModel):
    metrics_path: str
    persistence: PersistenceDriver
    is_production: bool
    is_threadsafe: bool
    logger: Logger

    class Config:
        arbitrary_types_allowed = True
