from abc import ABC, abstractmethod
from typing import Any, Dict


class PersistenceDriver(ABC):
    @abstractmethod
    def save_document(self, document: Dict[str, Any]) -> str:
        pass
