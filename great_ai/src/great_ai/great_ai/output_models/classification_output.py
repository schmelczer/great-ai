from typing import Any, Optional, Union

from pydantic import BaseModel


class ClassificationOutput(BaseModel):
    label: Union[str, int]
    confidence: float
    explanation: Optional[Any]

    def __hash__(self) -> int:
        return hash((type(self),) + tuple(self.__dict__.values()))
