from typing import Union

from pydantic import BaseModel

from .operators import Operator


class Filter(BaseModel):
    property: str
    operator: Operator
    value: Union[float, str]
