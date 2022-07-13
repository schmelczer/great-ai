from pydantic import BaseModel


class Match(BaseModel):
    phrase: str
    score: float
