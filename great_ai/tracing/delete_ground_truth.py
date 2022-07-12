from datetime import datetime
from typing import List, Optional, Union

from ..context import get_context


def delete_ground_truth(
    conjunctive_tags: Union[List[str], str] = [],
    *,
    since: Optional[datetime] = None,
    until: Optional[datetime] = None,
) -> None:
    """Delete traces matching the given criteria.

    Takes the same arguments as `query_ground_truth` but instead of returning them,
    it simply deletes them.

    You can rely on the efficiency of the delete's implementation.

    Examples:
        >>> delete_ground_truth(['train', 'test', 'validation'])

    Args:
        conjunctive_tags: Single tag or a list of tags which the deleted traces have to
            match. The relationship between the tags is conjunctive (AND).
        since: Only delete traces created after the given timestamp. `None` means no
            filtering.
        until: Only delete traces created before the given timestamp. `None` means no
            filtering.
    """

    tags = (
        conjunctive_tags if isinstance(conjunctive_tags, list) else [conjunctive_tags]
    )
    db = get_context().tracing_database

    items, length = db.query(
        conjunctive_tags=tags, until=until, since=since, has_feedback=True
    )

    db.delete_batch([i.trace_id for i in items])
