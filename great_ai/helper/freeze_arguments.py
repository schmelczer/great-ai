from functools import wraps
from typing import Any, Callable, Dict, List, Set, Union

from pydantic import BaseModel


class FrozenDict(dict):
    def __hash__(self) -> int:
        return hash(frozenset((k, freeze(v)) for k, v in self.items()))


class FrozenList(list):
    def __hash__(self) -> int:
        return hash(tuple(freeze(i) for i in self))


class FrozenSet(set):
    def __hash__(self) -> int:
        return hash(frozenset(freeze(i) for i in self))


def freeze_arguments(func: Callable[..., Any]) -> Callable[..., Any]:
    """Transform mutable dictionary
    Into immutable
    Useful to be compatible with cache
    source: https://stackoverflow.com/questions/6358481/using-functools-lru-cache-with-dictionary-arguments
    """

    @wraps(func)
    def wrapper(*args: List[Any], **kwargs: Dict[str, Any]) -> Any:
        args = tuple(freeze(arg) for arg in args)
        kwargs = {k: freeze(v) for k, v in kwargs.items()}
        return func(*args, **kwargs)

    return wrapper


def freeze(value: Union[List[Any], Dict[str, Any], Set[Any]]) -> Any:
    if isinstance(value, dict):
        return FrozenDict(value)

    if isinstance(value, list):
        return FrozenList(value)

    if isinstance(value, set):
        return FrozenSet(value)

    if isinstance(value, BaseModel):

        class HashableValue(type(value)):
            def __hash__(self) -> int:
                return hash(frozenset((k, freeze(v)) for k, v in self.dict().items()))

        return HashableValue(**value.dict())

    return value
