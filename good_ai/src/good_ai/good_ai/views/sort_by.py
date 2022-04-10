from typing import Literal
from typing_extensions import TypedDict


class SortBy(TypedDict):
    column_id: str
    direction: Literal["asc", "desc"]
