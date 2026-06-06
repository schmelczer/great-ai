from datetime import datetime
from typing import List, Optional, Union

from ..context import get_context
from ..views import Trace


def query_ground_truth(
    conjunctive_tags: Union[List[str], str] = [],
    *,
    since: Optional[datetime] = None,
    until: Optional[datetime] = None,
    return_max_count: Optional[int] = None,
) -> List[Trace]:
    """Return training samples.

    Combines, filters, and returns data-points that have been either added by
    `add_ground_truth` or were the result of a prediction after which their trace got
    feedback through the RESP API-s `/traces/{trace_id}/feedback` endpoint
    (end-to-end feedback).

    Filtering can be used to only return points matching all given tags (or the single
    given tag) and by time of creation.

    Examples:
        >>> query_ground_truth()
        [...]

    Args:
        conjunctive_tags: Single tag or a list of tags which the returned traces have to
            match. The relationship between the tags is conjunctive (AND).
        since: Only return traces created after the given timestamp. `None` means no
            filtering.
        until: Only return traces created before the given timestamp. `None` means no
            filtering.
        return_max_count: Return at-most this many traces. (take, limit)
    """

    tags = (
        conjunctive_tags if isinstance(conjunctive_tags, list) else [conjunctive_tags]
    )
    db = get_context().tracing_database

    items, length = db.query(
        conjunctive_tags=tags,
        since=since,
        until=until,
        take=return_max_count,
        has_feedback=True,
    )
    return items
