from typing import List

from ..hashable_base_model import HashableBaseModel
from .classification_output import ClassificationOutput


class MultiLabelClassificationOutput(HashableBaseModel):
    labels: List[ClassificationOutput] = []
