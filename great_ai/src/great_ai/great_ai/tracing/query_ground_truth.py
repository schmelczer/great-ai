from datetime import datetime
from typing import List, Optional, TypeVar, Union

from ..context import get_context
from ..views.trace import Trace

T = TypeVar("T")


def query_ground_truth(
    conjunctive_tags: Union[List[str], str] = [],
    *,
    since: Optional[datetime] = None,
    return_max_count: Optional[int] = None
) -> List[Trace[T]]:
    tags = (
        conjunctive_tags if isinstance(conjunctive_tags, list) else [conjunctive_tags]
    )
    db = get_context().tracing_database

    items, length = db.query(
        conjunctive_tags=tags, since=since, take=return_max_count, has_feedback=True
    )
    return items