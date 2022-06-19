from typing import Any, Optional, Union

from ..helper import HashableBaseModel


class ClassificationOutput(HashableBaseModel):
    label: Union[str, int]
    confidence: float
    explanation: Optional[Any]
