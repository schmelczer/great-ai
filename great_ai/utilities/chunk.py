from typing import Iterable, List, TypeVar

T = TypeVar("T")


def chunk(values: Iterable[T], chunk_size: int) -> Iterable[List[T]]:
    """Turn an iterable of items into an iterable of lists (chunks) of items.

    Each returned chunk is of length `chunk_size` except the last one the length of
    which is between 1 and `chunk_size`.

    Useful for parallel processing.

    Examples:
        >>> list(chunk(range(10), chunk_size=3))
        [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]

    Args:
        values: The stream of items to pack into chunks.
        chunk_size: Desired length of each (but the last) chunk.

    Yields:
        The next chunk.
    """

    assert chunk_size >= 1

    result: List[T] = []
    for v in values:
        result.append(v)
        if len(result) == chunk_size:
            yield result
            result = []

    if len(result) > 0:
        yield result
