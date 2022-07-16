from typing import Any, NamedTuple, Optional


class MapResult(NamedTuple):
    order: int
    value: Any
    exception: Optional[str] = None
    worker_traceback: Optional[str] = None
