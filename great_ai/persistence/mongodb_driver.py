from datetime import datetime
from typing import Any, Dict, List, Optional, Sequence, Tuple

from pymongo import ASCENDING, DESCENDING, MongoClient

from ..utilities import chunk
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


class MongoDbDriver(TracingDatabaseDriver):
    """TracingDatabaseDriver implementation using MongoDB as a backend.

    A production-ready database driver suitable for efficiently handling semi-structured
    data.

    Checkout [MongoDB Atlas](https://www.mongodb.com/cloud/atlas/register) for a hosted
    MongoDB solution.
    """

    is_production_ready = True

    mongo_connection_string: str
    mongo_database: str

    def __init__(self) -> None:
        super().__init__()
        if self.mongo_connection_string is None or self.mongo_database is None:
            raise ValueError(
                "Please configure the MongoDB access options by calling "
                "MongoDbDriver.configure_credentials"
            )

        with MongoClient[Any](self.mongo_connection_string) as client:
            client[self.mongo_database].traces.create_index(
                [("tags", ASCENDING), ("created", DESCENDING)], background=True
            )

    @classmethod
    def configure_credentials(  # type: ignore
        cls,
        *,
        mongo_connection_string: str,
        mongo_database: str,
        **_: Any,
    ) -> None:
        """Configure the connection details for MongoDB.

        Args:
            mongo_connection_string: For example:
                'mongodb://my_user:my_pass@localhost:27017'
            mongo_database: Name of the database to use. If doesn't exist, it is
                created and initialised.
        """
        cls.mongo_connection_string = mongo_connection_string
        cls.mongo_database = mongo_database
        super().configure_credentials()

    def save(self, trace: Trace) -> str:
        serialized = trace.to_flat_dict()
        serialized["_id"] = trace.trace_id

        with MongoClient[Any](self.mongo_connection_string) as client:
            return client[self.mongo_database].traces.insert_one(serialized).inserted_id

    def save_batch(self, documents: List[Trace]) -> List[str]:
        serialized = [d.to_flat_dict() for d in documents]
        for s in serialized:
            s["_id"] = s["trace_id"]

        with MongoClient[Any](self.mongo_connection_string) as client:
            return (
                client[self.mongo_database]
                .traces.insert_many(serialized, ordered=False)
                .inserted_ids
            )

    def get(self, id: str) -> Optional[Trace]:
        with MongoClient[Any](self.mongo_connection_string) as client:
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

        query: Dict[str, Any] = {
            "filter": {},
        }

        and_query: List[Dict[str, Any]] = []
        and_query.extend({"tags": tag} for tag in conjunctive_tags)
        and_query.extend(
            {f.property: {self._get_operator(f): f.value}} for f in conjunctive_filters
        )
        if not and_query:
            and_query.append({})

        if since:
            and_query.append({"created": {"$gte": since}})

        if until:
            and_query.append({"created": {"$lte": until}})

        if has_feedback is not None:
            and_query.append(
                {"feedback": {"$ne": None}} if has_feedback else {"feedback": None}
            )
        query["filter"]["$and"] = and_query

        with MongoClient[Any](self.mongo_connection_string) as client:
            count = client[self.mongo_database].traces.count_documents(**query)

            if skip:
                query["skip"] = skip

            if take:
                query["limit"] = take

            query["sort"] = [
                (col.column_id, 1 if col.direction == "asc" else -1) for col in sort_by
            ]

            with client[self.mongo_database].traces.find(**query) as cursor:
                documents = [Trace[Any].parse_obj(t) for t in cursor]
        return documents, count

    def update(self, id: str, new_version: Trace) -> None:
        serialized = new_version.to_flat_dict()
        serialized["_id"] = new_version.trace_id

        with MongoClient[Any](self.mongo_connection_string) as client:
            client[self.mongo_database].traces.update_one({"_id": id}, serialized)

    def delete(self, id: str) -> None:
        with MongoClient[Any](self.mongo_connection_string) as client:
            client[self.mongo_database].traces.delete_one({"_id": id})

    def delete_batch(self, ids: List[str]) -> None:
        with MongoClient[Any](self.mongo_connection_string) as client:
            for c in chunk(
                ids, chunk_size=10000
            ):  # avoid: 'delete' command document too large
                delete_filter = {"_id": {"$in": c}}
                client[self.mongo_database].traces.delete_many(delete_filter)
