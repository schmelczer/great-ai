from pydantic import BaseModel

from ..persistence import PersistenceDriver


class Context(BaseModel):
    metrics_path: str
    persistence: PersistenceDriver
    is_production: bool
    is_threadsafe: bool

    class Config:
        arbitrary_types_allowed = True
