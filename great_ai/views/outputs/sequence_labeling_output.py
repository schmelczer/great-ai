from typing import Any, List, Literal, Optional

from ..hashable_base_model import HashableBaseModel


class LabeledToken(HashableBaseModel):
    token: str
    tag: Literal["B", "I", "O", "E", "S"]
    confidence: float
    explanation: Optional[Any]


class SequenceLabelingOutput(HashableBaseModel):
    labeled_tokens: List[LabeledToken]
    explanation: Optional[Any]
