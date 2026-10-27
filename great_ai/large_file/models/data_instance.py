from typing import Any, Optional

from pydantic import BaseModel


class DataInstance(BaseModel):
    name: str
    version: int
    remote_path: Any
    cache_identity: Optional[str] = None
