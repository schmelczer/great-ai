from datetime import datetime
from typing import List, Optional, Sequence

from pydantic import BaseModel

from .filter import Filter
from .sort_by import SortBy


class Query(BaseModel):
    filter: List[Filter] = []
    sort: List[SortBy] = []
    conjunctive_tags: Sequence[str] = []
    since: Optional[datetime] = None
    until: Optional[datetime] = None
    has_feedback: Optional[bool] = None

    class Config:
        schema_extra = {
            "example": {
                "filter": [
                    {
                        "property": "original_execution_time_ms",
                        "operator": ">",
                        "value": 100,
                    }
                ],
                "sort": [
                    {"column_id": "original_execution_time_ms", "direction": "asc"},
                    {"column_id": "id", "direction": "desc"},
                ],
                "conjunctive_tags": ["online"],
                "has_feedback": False,
            }
        }
