from typing import List, Literal, Union

from pydantic import BaseModel

from .text import Text


class Title(BaseModel):
    text: Text


class Paragraph(BaseModel):
    sentences: List[Text]


MetaType = Literal[
    "abstract_start",
    "abstract_end",
    "acknowledgements_start",
    "acknowledgements_end",
    "annex_start",
    "annex_end",
]


class Meta(BaseModel):
    meta_type: MetaType


Element = Union[Title, Paragraph, Meta]
