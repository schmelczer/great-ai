from multiprocessing import Lock
from pathlib import Path
from typing import Any, Callable, Optional, Sequence, Tuple

import pandas as pd
from tinydb import TinyDB

from ..views import Filter, SortBy, Trace
from .tracing_database import TracingDatabase

lock = Lock()


operator_mapping = {"=": "eq", "!=": "ne", "<": "lt", "<=": "le", ">": "gt", ">=": "ge"}


class ParallelTinyDbDriver(TracingDatabase):
    is_threadsafe = True

    def __init__(self, path_to_db: Path) -> None:
        super().__init__()
        self._path_to_db = path_to_db

    def save(self, trace: Trace) -> str:
        return self._safe_execute(lambda db: db.insert(trace.dict()))

    def get(self, id: str) -> Optional[Trace]:
        value = self._safe_execute(lambda db: db.get(lambda d: d["trace_id"] == id))
        if value:
            value = Trace.parse_obj(value)
        return value

    def query(
        self,
        skip: int = 0,
        take: Optional[int] = None,
        conjunctive_filters: Sequence[Filter] = [],
        sort_by: Sequence[SortBy] = [],
    ) -> Tuple[Sequence[Trace], int]:
        documents = [
            Trace.parse_obj(t) for t in self._safe_execute(lambda db: db.all())
        ]

        if not documents:
            return [], 0

        df = pd.DataFrame([d.to_flat_dict() for d in documents])

        for f in conjunctive_filters:
            operator = f.operator.lower()
            if operator in operator_mapping:
                df = df.loc[
                    getattr(df[f.property], operator_mapping[f.operator])(f.value)
                ]
            elif operator == "contains":
                df = df.loc[df[f.property].str.contains(f.value, case=False)]

        if sort_by:
            df.sort_values(
                [col["column_id"] for col in sort_by],
                ascending=[col["direction"] == "asc" for col in sort_by],
                inplace=True,
            )

        count = len(df)
        result = df.iloc[skip:] if take is None else df.iloc[skip : skip + take]
        return [
            next(d for d in documents if d.trace_id == trace_id)
            for trace_id in result["trace_id"]
        ], count

    def update(self, id: str, new_version: Trace) -> None:
        self._safe_execute(
            lambda db: db.update(new_version.dict(), lambda d: d["trace_id"] == id)
        )

    def delete(self, id: str) -> None:
        self._safe_execute(lambda db: db.remove(lambda d: d["trace_id"] == id))

    def _safe_execute(self, func: Callable[[TinyDB], Any]) -> Any:
        with lock:
            with TinyDB(self._path_to_db) as db:
                return func(db)
