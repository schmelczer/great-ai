import inspect
from functools import lru_cache, wraps
from typing import Any, Callable, Mapping, Sequence, Set, Type, TypeVar, Union, cast

from pydantic import BaseModel

F = TypeVar("F", bound=Callable)


@lru_cache(maxsize=None)
def _hashable_model_type(model_type: Type[BaseModel]) -> Type[BaseModel]:
    # The subclass is cached per model type: Pydantic v2's __eq__ requires both
    # operands to share a type, so creating a fresh subclass on every freeze()
    # call would make even identical models compare unequal.
    class HashableValue(model_type):  # type: ignore
        __slots__ = ()

        def __hash__(self) -> int:
            return hash(freeze(self.model_dump()))

    return HashableValue


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
        # Keep the already-validated values, aliases, nested types and private
        # attributes. Reconstructing from model_dump() runs validators again.
        frozen = value.model_copy()
        object.__setattr__(frozen, "__class__", _hashable_model_type(type(value)))
        return frozen

    return value
