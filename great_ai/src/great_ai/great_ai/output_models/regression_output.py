from typing import Any, Optional, Union

from pydantic import BaseModel


class RegressionOutput(BaseModel):
    value: Union[int, float]
    explanation: Optional[Any]

    def __hash__(self) -> int:
        return hash((type(self),) + tuple(self.__dict__.values()))
