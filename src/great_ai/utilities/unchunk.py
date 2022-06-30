from typing import Iterable, TypeVar

T = TypeVar("T")


def unchunk(chunks: Iterable[Iterable[T]]) -> Iterable[T]:
    for chunk in chunks:
        yield from chunk
