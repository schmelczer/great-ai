from typing import Literal, TypedDict


class SortBy(TypedDict):
    column_id: str
    direction: Literal["asc", "desc"]
