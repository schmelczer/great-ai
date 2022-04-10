from typing import List

from pydantic import BaseModel

from .filter import Filter
from .sort_by import SortBy


class Query(BaseModel):
    filter: List[Filter] = []
    sort: List[SortBy] = []
    skip: int = 0
    take: int = 100
