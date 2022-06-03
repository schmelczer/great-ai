from typing import Any, Literal

from pydantic import BaseModel


class DataInstance(BaseModel):
    name: str
    version: int
    remote_path: Any
    origin: Literal["filesystem", "mongodb", "s3"]
