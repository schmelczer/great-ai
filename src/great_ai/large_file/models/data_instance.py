from typing import Any

from pydantic import BaseModel


class DataInstance(BaseModel):
    name: str
    version: int
    remote_path: Any
