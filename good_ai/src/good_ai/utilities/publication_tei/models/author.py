from typing import List, Optional

from pydantic import BaseModel

from .affiliation import Affiliation


class Author(BaseModel):
    name: Optional[str]
    orcid: Optional[str]
    email: Optional[str]
    corresponding: bool
    affiliations: List[Affiliation]
    coordinates: Optional[str]
