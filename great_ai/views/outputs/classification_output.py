from typing import Any, Optional, Union

from ..hashable_base_model import HashableBaseModel


class ClassificationOutput(HashableBaseModel):
    label: Union[str, int]
    confidence: float
    explanation: Optional[Any]
