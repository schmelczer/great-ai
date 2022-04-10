from abc import ABC, abstractmethod
from typing import Any, Dict

from black import List

from ..views import Filter, SortBy, Trace


class PersistenceDriver(ABC):
    is_threadsafe: bool

    @abstractmethod
    def save_document(self, document: Trace) -> str:
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
        sort_by: List[SortBy],
        skip: int,
        take: int,
    ) -> List[Dict[str, Any]]:
        pass
