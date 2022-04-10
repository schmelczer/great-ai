from multiprocessing import Lock
from pathlib import Path
from typing import Any, Callable, Dict

import pandas as pd
from black import List
from tinydb import TinyDB

from ..views import Filter, SortBy, Trace
from .persistence_driver import PersistenceDriver

lock = Lock()


operator_mapping = {"=": "eq", "!=": "ne", "<": "lt", "<=": "le", ">": "gt", ">=": "ge"}


class ParallelTinyDbDriver(PersistenceDriver):
    is_threadsafe = True

    def __init__(self, path_to_db: Path) -> None:
        super().__init__()
        self._path_to_db = path_to_db

    def save_document(self, trace: Trace) -> str:
        return self._safe_execute(lambda db: db.insert(trace.dict()))

    def get_traces(self) -> List[Trace]:
        return self._safe_execute(lambda db: [Trace.parse_obj(t) for t in db.all()])

    def get_documents(self) -> List[Dict[str, Any]]:
        documents = self.get_traces()
        return [d.to_flat_dict() for d in documents]

    def query(
        self,
        conjunctive_filters: List[Filter],
        sort_by: List[SortBy],
        skip: int,
        take: int,
    ) -> List[Dict[str, Any]]:
        documents = self.get_documents()
        df = pd.DataFrame(documents)

        for f in conjunctive_filters:
            if f.operator in operator_mapping:
                df = df.loc[
                    getattr(df[f.property], operator_mapping[f.operator])(f.value)
                ]
            elif f.operator == "contains":
                df = df.loc[df[f.property].str.contains(f.value)]

        if sort_by:
            df = df.sort_values(
                [col["column_id"] for col in sort_by],
                ascending=[col["direction"] == "asc" for col in sort_by],
                inplace=False,
            )

        return df.iloc[skip : skip + take].to_dict("records")

    def _safe_execute(self, func: Callable[[TinyDB], Any]) -> Any:
        with lock:
            with TinyDB(self._path_to_db) as db:
                return func(db)
