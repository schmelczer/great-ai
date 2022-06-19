from typing import List

from ..helper import HashableBaseModel
from .classification_output import ClassificationOutput


class MultiLabelClassificationOutput(HashableBaseModel):
    labels: List[ClassificationOutput] = []
