from typing import Any

from pydantic import BaseModel


class ApiMetadata(BaseModel):
    name: str
    version: str
    documentation: str
    configuration: Any
