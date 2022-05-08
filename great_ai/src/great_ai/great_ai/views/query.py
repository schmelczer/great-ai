from typing import List

from pydantic import BaseModel

from .filter import Filter
from .sort_by import SortBy


class Query(BaseModel):
    filter: List[Filter] = []
    sort: List[SortBy] = []
    skip: int = 0
    take: int = 100

    class Config:
        schema_extra = {
            "example": {
                "filter": [
                    {"property": "execution_time_ms", "operator": ">", "value": 100}
                ],
                "sort": [
                    {"column_id": "execution_time_ms", "direction": "asc"},
                    {"column_id": "id", "direction": "desc"},
                ],
                "take": 10,
            }
        }
