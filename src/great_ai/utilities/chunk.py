from typing import Iterable, List, TypeVar

T = TypeVar("T")


def chunk(values: Iterable[T], chunk_length: int) -> Iterable[T]:
    assert chunk_length >= 1

    result: List[T] = []
    for v in values:
        result.append(v)
        if len(result) == chunk_length:
            yield result
            result = []

    if len(result) > 0:
        yield result
