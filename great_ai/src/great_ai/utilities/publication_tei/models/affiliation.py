from typing import Optional, Tuple

from pydantic import BaseModel


class Affiliation(BaseModel):
    institutions: Tuple[str, ...]
    departments: Tuple[str, ...]
    laboratories: Tuple[str, ...]
    country: Optional[str]
    settlement: Optional[str]
