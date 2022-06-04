from abc import ABC, abstractmethod
from typing import Optional, Sequence, Tuple

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
        conjunctive_filters: Sequence[Filter] = [],
        sort_by: Sequence[SortBy] = [],
    ) -> Tuple[Sequence[Trace], int]:
        pass

    @abstractmethod
    def update(self, id: str, new_version: Trace) -> None:
        pass

    @abstractmethod
    def delete(self, id: str) -> None:
        pass
