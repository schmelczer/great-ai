from typing import Any, Optional, Union

from ..hashable_base_model import HashableBaseModel


class RegressionOutput(HashableBaseModel):
    value: Union[int, float]
    explanation: Optional[Any]
