from abc import ABC, abstractmethod
from typing import List, Optional

from ..views import Filter, SortBy, Trace


class TracingDatabase(ABC):
    is_threadsafe: bool

    @abstractmethod
    def save(self, document: Trace) -> str:
        pass

    @abstractmethod
    def get(self, id: str) -> Optional[Trace]:
        pass

    @abstractmethod
    def query(
        self,
        skip: int = 0,
        take: Optional[int] = None,
        conjunctive_filters: List[Filter] = [],
        sort_by: List[SortBy] = [],
    ) -> List[Trace]:
        pass

    @abstractmethod
    def update(self, id: str, new_version: Trace) -> None:
        pass

    @abstractmethod
    def delete(self, id: str) -> None:
        pass
