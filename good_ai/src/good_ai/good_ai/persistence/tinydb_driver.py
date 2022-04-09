from pathlib import Path
from typing import Any, Dict

from tinydb import TinyDB

from .persistence_driver import PersistenceDriver


class TinyDbDriver(PersistenceDriver):
    def __init__(self, path_to_db: Path) -> None:
        super().__init__()
        self._db = TinyDB(path_to_db)

    def save_document(self, document: Dict[str, Any]) -> str:
        return self._db.insert(document)
