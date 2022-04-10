from pathlib import Path
from typing import Any, Callable
from black import List
from tinydb import TinyDB
from multiprocessing import Process, Lock

from ..views import Trace
from .persistence_driver import PersistenceDriver


lock = Lock()


class ParallelTinyDbDriver(PersistenceDriver):
    is_threadsafe = True
    
    def __init__(self, path_to_db: Path) -> None:
        super().__init__()
        self._path_to_db = path_to_db

    def save_document(self, trace: Trace) -> str:
        return self._safe_execute(lambda db: db.insert(trace.dict()))

    def get_documents(self) -> List[Trace]:
        return self._safe_execute(lambda db: [Trace.parse_obj(t) for t in db.all()])

    def _safe_execute(self, func: Callable[[TinyDB], Any]) -> Any:
        with lock:
            with TinyDB(self._path_to_db) as db:
                return func(db)
