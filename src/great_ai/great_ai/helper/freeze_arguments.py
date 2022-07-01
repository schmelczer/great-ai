from functools import wraps
from typing import Any, Callable, Dict, List, Set, Union


class FrozenDict(dict):
    def __hash__(self) -> int:
        return hash(frozenset(self.items()))


class FrozenList(list):
    def __hash__(self) -> int:
        return hash(tuple(self))


class FrozenSet(set):
    def __hash__(self) -> int:
        return hash(frozenset(self))


def freeze_arguments(func: Callable[..., Any]) -> Callable[..., Any]:
    """Transform mutable dictionary
    Into immutable
    Useful to be compatible with cache
    source: https://stackoverflow.com/questions/6358481/using-functools-lru-cache-with-dictionary-arguments
    """

    @wraps(func)
    def wrapper(*args: List[Any], **kwargs: Dict[str, Any]) -> Any:
        args = tuple(_freeze(arg) for arg in args)
        kwargs = {k: _freeze(v) for k, v in kwargs.items()}
        return func(*args, **kwargs)

    return wrapper


def _freeze(value: Union[List[Any], Dict[str, Any], Set[Any]]) -> Any:
    if isinstance(value, dict):
        return FrozenDict(value)

    if isinstance(value, list):
        return FrozenList(value)

    if isinstance(value, set):
        return FrozenSet(value)

    return value
