from pydantic import BaseModel


class Model(BaseModel):
    key: str
    version: int
