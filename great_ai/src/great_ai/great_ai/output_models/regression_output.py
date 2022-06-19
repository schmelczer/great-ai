from typing import Any, Optional, Union

from ..helper import HashableBaseModel


class RegressionOutput(HashableBaseModel):
    value: Union[int, float]
    explanation: Optional[Any]
