from datetime import datetime
from multiprocessing import Lock
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple

import pandas as pd
from tinydb import TinyDB

from ..views import Filter, SortBy, Trace
from .tracing_database_driver import TracingDatabaseDriver

DEFAULT_TRACING_DB_FILENAME = "tracing_database.json"
lock = Lock()


operator_mapping = {"=": "eq", "!=": "ne", "<": "lt", "<=": "le", ">": "gt", ">=": "ge"}


class ParallelTinyDbDriver(TracingDatabaseDriver):
    """TracingDatabaseDriver with TinyDB as a backend.

    Saves the database as a JSON into a single file. Highly inefficient on inserting,
    not advised for production use.

    A multiprocessing lock protects the database file to avoid parallelisation issues.
    """

    is_production_ready = False
    path_to_db = Path(DEFAULT_TRACING_DB_FILENAME)

    def save(self, trace: Trace) -> str:
        return self._safe_execute(lambda db: db.insert(trace.dict()))

    def save_batch(self, documents: List[Trace]) -> List[str]:
        traces = [d.dict() for d in documents]
        return self._safe_execute(lambda db: db.insert_multiple(traces))

    def get(self, id: str) -> Optional[Trace]:
        value = self._safe_execute(lambda db: db.get(lambda d: d["trace_id"] == id))
        if value:
            value = Trace.parse_obj(value)
        return value

    def query(
        self,
        *,
        skip: int = 0,
        take: Optional[int] = None,
        conjunctive_filters: Sequence[Filter] = [],
        conjunctive_tags: Sequence[str] = [],
        since: Optional[datetime] = None,
        until: Optional[datetime] = None,
        has_feedback: Optional[bool] = None,
        sort_by: Sequence[SortBy] = []
    ) -> Tuple[List[Trace], int]:
        def does_match(d: Dict[str, Any]) -> bool:
            return (
                not set(conjunctive_tags) - set(d["tags"])
                and (since is None or datetime.fromisoformat(d["created"]) >= since)
                and (until is None or datetime.fromisoformat(d["created"]) <= until)
                and (
                    has_feedback is None or has_feedback == (d["feedback"] is not None)
                )
            )

        documents: List[Trace] = [
            Trace.parse_obj(t)
            for t in self._safe_execute(lambda db: db.search(does_match))
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
                [col.column_id for col in sort_by],
                ascending=[col.direction == "asc" for col in sort_by],
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

    def delete_batch(self, ids: List[str]) -> None:
        for i in ids:
            self.delete(i)

    def _safe_execute(self, func: Callable[[TinyDB], Any]) -> Any:
        with lock:
            with TinyDB(self.path_to_db) as db:
                return func(db)
