from typing import List

from pydantic import BaseModel


class NameParts(BaseModel):
    first_names: List[str]
    initials: List[str]
    infixes: List[str]
    last_names: List[str]
