from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional, Sequence, Tuple

from ..views import Filter, SortBy, Trace


class TracingDatabaseDriver(ABC):
    is_production_ready: bool

    @abstractmethod
    def save(self, document: Trace) -> str:
        pass

    @abstractmethod
    def save_batch(
        self,
        documents: List[Trace],
    ) -> List[str]:
        pass

    @abstractmethod
    def get(self, id: str) -> Optional[Trace]:
        pass

    @abstractmethod
    def query(
        self,
        *,
        skip: int = 0,
        take: Optional[int] = None,
        conjunctive_filters: Sequence[Filter] = [],
        conjunctive_tags: Sequence[str] = [],
        since: Optional[datetime] = None,
        sort_by: Sequence[SortBy] = [],
        has_feedback: Optional[bool] = None
    ) -> Tuple[List[Trace], int]:
        pass

    @abstractmethod
    def update(self, id: str, new_version: Trace) -> None:
        pass

    @abstractmethod
    def delete(self, id: str) -> None:
        pass
