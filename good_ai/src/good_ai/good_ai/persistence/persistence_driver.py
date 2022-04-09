from abc import ABC, abstractmethod

from black import List

from good_ai.good_ai.views.trace import Trace


class PersistenceDriver(ABC):
    @abstractmethod
    def save_document(self, document: Trace) -> str:
        pass

    @abstractmethod
    def get_documents(self) -> List[Trace]:
        pass
