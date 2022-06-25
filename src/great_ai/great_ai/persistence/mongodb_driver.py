from datetime import datetime
from typing import Any, List, Mapping, Optional, Sequence, Tuple

from pymongo import MongoClient

from ..views import Filter, SortBy, Trace
from .tracing_database_driver import TracingDatabaseDriver

operator_mapping = {
    "=": "$eq",
    "!=": "$ne",
    "<": "$lt",
    "<=": "$lte",
    ">": "$gt",
    ">=": "$gte",
    "contains": "$regex",
}


class MongodbDriver(TracingDatabaseDriver):
    is_production_ready = True

    def __init__(self) -> None:
        super().__init__()
        if self.mongo_connection_string is None or self.mongo_database is None:
            raise ValueError(
                "Please configure the MongoDB access options by calling MongodbDriver.configure_credentials"
            )

    @classmethod
    def configure_credentials(  # type: ignore
        cls,
        *,
        mongo_connection_string: str,
        mongo_database: str,
        **_: Mapping[str, Any],
    ) -> None:
        cls.mongo_connection_string = mongo_connection_string
        cls.mongo_database = mongo_database
        super().configure_credentials()

    def save(self, trace: Trace) -> str:
        serialized = trace.to_flat_dict()
        serialized["_id"] = trace.trace_id

        with MongoClient(self.mongo_connection_string) as client:
            return client[self.mongo_database].traces.insert_one(serialized)

    def save_batch(self, documents: List[Trace]) -> List[str]:
        serialized = [d.to_flat_dict() for d in documents]
        for s in serialized:
            s["_id"] = s["trace_id"]

        with MongoClient(self.mongo_connection_string) as client:
            return client[self.mongo_database].traces.insert_many(
                serialized, ordered=False
            )

    def get(self, id: str) -> Optional[Trace]:
        with MongoClient(self.mongo_connection_string) as client:
            value = client[self.mongo_database].traces.find_one(id)

        if value:
            value = Trace.parse_obj(value)

        return value

    def _get_operator(self, filter: Filter) -> str:
        if filter.operator == "contains" and not isinstance(filter.value, str):
            return operator_mapping["="]
        return operator_mapping[filter.operator]

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
        sort_by: Sequence[SortBy] = [],
    ) -> Tuple[List[Trace], int]:

        query = {
            "filter": {
                "$and": [{"tags": tag} for tag in conjunctive_tags]
                + [
                    {f.property: {self._get_operator(f): f.value}}
                    for f in conjunctive_filters
                ]
                + [{}]
            },
            "sort": [
                (col.column_id, 1 if col.direction == "asc" else -1) for col in sort_by
            ],
        }

        if skip:
            query["skip"] = skip

        if take:
            query["limit"] = take

        if since:
            query["filter"]["$and"].append({"created": {"$gte": since}})

        if until:
            query["filter"]["$and"].append({"created": {"$lte": until}})

        if has_feedback is not None:
            query["filter"]["$and"].append(
                {"feedback": {"$ne": None}} if has_feedback else {"feedback": None}
            )

        with MongoClient(self.mongo_connection_string) as client:
            values = client[self.mongo_database].traces.find(**query)
            documents = [Trace.parse_obj(t) for t in values]

        return documents, len(documents)

    def update(self, id: str, new_version: Trace) -> None:
        serialized = new_version.dict()
        serialized["_id"] = new_version.trace_id
        with MongoClient(self.mongo_connection_string) as client:
            client[self.mongo_database].traces.update_one(id, new_version)

    def delete(self, id: str) -> None:
        with MongoClient(self.mongo_connection_string) as client:
            client[self.mongo_database].traces.delete_one(id)

    def delete_batch(self, ids: List[str]) -> List[str]:
        delete_filter = {"_id": {"$in": ids}}

        with MongoClient(self.mongo_connection_string) as client:
            return client[self.mongo_database].traces.delete_many(delete_filter)
