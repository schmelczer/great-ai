from pathlib import Path
from uuid import uuid4

from black import List
from tinydb import TinyDB
from tinydb.table import Document

from ..views import Trace
from .persistence_driver import PersistenceDriver


class TinyDbDriver(PersistenceDriver):
    is_threadsafe = False
    
    def __init__(self, path_to_db: Path) -> None:
        super().__init__()
        self._db = TinyDB(path_to_db)

    def save_document(self, trace: Trace) -> str:
        return self._db.insert(trace.dict())

    def get_documents(self) -> List[Trace]:
        return [Trace.parse_obj(t) for t in self._db.all()]
