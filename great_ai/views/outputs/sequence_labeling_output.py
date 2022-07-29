from typing import Any, List, Optional

from typing_extensions import Literal  # <= Python 3.7

from ..hashable_base_model import HashableBaseModel


class LabeledToken(HashableBaseModel):
    token: str
    tag: Literal["B", "I", "O", "E", "S"]
    confidence: float
    explanation: Optional[Any]


class SequenceLabelingOutput(HashableBaseModel):
    labeled_tokens: List[LabeledToken]
    explanation: Optional[Any]
