from typing import Literal

from pydantic import BaseModel


class SortBy(BaseModel):
    column_id: str
    direction: Literal["asc", "desc"]
