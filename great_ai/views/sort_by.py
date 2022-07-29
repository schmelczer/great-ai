from pydantic import BaseModel
from typing_extensions import Literal  # <= Python 3.7


class SortBy(BaseModel):
    column_id: str
    direction: Literal["asc", "desc"]
