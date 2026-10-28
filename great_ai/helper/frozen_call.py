from copy import deepcopy
from typing import Any, Dict, Tuple

import numpy as np
from pydantic import BaseModel


def make_hashable(value: Any) -> Any:
    """Build an immutable value key without retaining mutable container contents."""
    if isinstance(value, np.ndarray):
        contents = (
            make_hashable(value.tolist()) if value.dtype.hasobject else value.tobytes()
        )
        return type(value), value.dtype, value.shape, contents
    if isinstance(value, np.generic):
        return type(value), value.dtype, value.tobytes()
    if isinstance(value, BaseModel):
        return type(value), make_hashable(value.model_dump())
    if isinstance(value, dict):
        return dict, frozenset(
            (make_hashable(k), make_hashable(v)) for k, v in value.items()
        )
    if isinstance(value, (list, tuple)):
        return (list if isinstance(value, list) else tuple), tuple(
            make_hashable(v) for v in value
        )
    if isinstance(value, (set, frozenset)):
        return set, frozenset(make_hashable(v) for v in value)
    return type(value), value


class FrozenCall:
    """Keep immutable cache identity separate from arguments used by a prediction."""

    def __init__(
        self, args: Tuple[Any, ...], kwargs: Dict[str, Any], do_not_persist: bool
    ) -> None:
        self._key = make_hashable((args, kwargs, do_not_persist))
        self.args, self.kwargs = deepcopy((args, kwargs))
        self.do_not_persist = do_not_persist

    def __hash__(self) -> int:
        return hash(self._key)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, FrozenCall):
            return NotImplemented
        return bool(self._key == other._key)
