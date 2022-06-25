from functools import wraps
from typing import Any, Callable, Dict, List


class FrozenDict(dict):
    def __hash__(self) -> int:  # type: ignore
        return hash(frozenset(self.items()))


def freeze_arguments(func: Callable[..., Any]) -> Callable[..., Any]:
    """Transform mutable dictionary
    Into immutable
    Useful to be compatible with cache
    source: https://stackoverflow.com/questions/6358481/using-functools-lru-cache-with-dictionary-arguments
    """

    @wraps(func)
    def wrapper(*args: List[Any], **kwargs: Dict[str, Any]) -> Any:
        args = tuple(FrozenDict(arg) if isinstance(arg, dict) else arg for arg in args)
        kwargs = {
            k: FrozenDict(v) if isinstance(v, dict) else v for k, v in kwargs.items()
        }
        return func(*args, **kwargs)

    return wrapper
