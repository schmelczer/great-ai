import builtins
from typing import Union

from pydantic import BaseModel

from .operators import Operator


class Filter(BaseModel):
    property: str
    operator: Operator
    value: Union[float, str]

    @builtins.property
    def value_as_text(self) -> str:
        if isinstance(self.value, float) and self.value.is_integer():
            return str(int(self.value))
        return str(self.value)
