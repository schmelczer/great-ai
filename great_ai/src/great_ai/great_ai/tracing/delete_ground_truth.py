from datetime import datetime
from typing import List, Optional, Union

from ..context import get_context


def delete_ground_truth(
    conjunctive_tags: Union[List[str], str] = [],
    *,
    until: Optional[datetime] = None,
    since: Optional[datetime] = None,
) -> None:
    tags = (
        conjunctive_tags if isinstance(conjunctive_tags, list) else [conjunctive_tags]
    )
    db = get_context().tracing_database

    items, length = db.query(
        conjunctive_tags=tags, until=until, since=since, has_feedback=True
    )

    db.delete_batch([i.trace_id for i in items])
