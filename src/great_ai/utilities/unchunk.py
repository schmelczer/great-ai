from typing import Iterable, Optional, TypeVar

T = TypeVar("T")


def unchunk(chunks: Iterable[Optional[Iterable[T]]]) -> Iterable[T]:
    for chunk in chunks:
        if chunk is not None:
            yield from chunk
