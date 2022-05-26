from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from ..views import Filter, SortBy, Trace


class PersistenceDriver(ABC):
    is_threadsafe: bool

    @abstractmethod
    def save_trace(self, document: Trace) -> str:
        pass

    @abstractmethod
    def add_evaluation(self, id: str, evaluation: Any) -> None:
        pass

    @abstractmethod
    def get_trace(self, id: str) -> Optional[Trace]:
        pass

    @abstractmethod
    def get_traces(self) -> List[Trace]:
        pass

    @abstractmethod
    def get_documents(self) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def query(
        self,
        conjunctive_filters: List[Filter],
        sort_by: List[SortBy] = [],
        skip: int = 0,
        take: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        pass
