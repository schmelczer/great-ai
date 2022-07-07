import inspect
from functools import wraps
from typing import Any, Callable, Mapping, Sequence, Set, TypeVar, Union, cast

from pydantic import BaseModel

F = TypeVar("F", bound=Callable)


class FrozenDict(dict):
    def __hash__(self) -> int:  # type: ignore
        return hash(frozenset((k, freeze(v)) for k, v in self.items()))


class FrozenList(list):
    def __hash__(self) -> int:  # type: ignore
        return hash(tuple(freeze(i) for i in self))


class FrozenSet(set):
    def __hash__(self) -> int:  # type: ignore
        return hash(frozenset(freeze(i) for i in self))


def freeze_arguments(func: F) -> F:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        args = tuple(freeze(arg) for arg in args)
        kwargs = {k: freeze(v) for k, v in kwargs.items()}
        return func(*args, **kwargs)

    @wraps(func)
    async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
        return await wrapper(*args, **kwargs)

    return cast(F, async_wrapper if inspect.iscoroutinefunction(func) else wrapper)


def freeze(value: Union[Sequence[Any], Mapping[str, Any], Set[Any], BaseModel]) -> Any:
    """
    >>> class MyClass(BaseModel):
    ...     a: int
    >>> my_object = MyClass(a=3)
    >>> my_other_object = MyClass(a=4)
    >>> freeze(my_object) == freeze(my_other_object), freeze(my_object) == freeze(my_object)
    (False, True)
    """
    if isinstance(value, dict):
        return FrozenDict(value)

    if isinstance(value, list):
        return FrozenList(value)

    if isinstance(value, set):
        return FrozenSet(value)

    if isinstance(value, BaseModel):

        class HashableValue(type(value)):  # type: ignore
            def __hash__(self) -> int:
                return hash(frozenset((k, freeze(v)) for k, v in self.dict().items()))

        return HashableValue(**value.dict())

    return value
