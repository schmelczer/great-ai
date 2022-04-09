from pydantic import BaseModel

from ..persistence import PersistenceDriver


class Context(BaseModel):
    metrics_path: str
    persistence: PersistenceDriver
    is_production: bool

    class Config:
        arbitrary_types_allowed = True
