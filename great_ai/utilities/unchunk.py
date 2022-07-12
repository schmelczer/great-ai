from typing import Iterable, Optional, TypeVar

T = TypeVar("T")


def unchunk(chunks: Iterable[Optional[Iterable[T]]]) -> Iterable[T]:
    """Turn a stream of chunks of items into a stream of items (flatten operation).

    The inverse operation of [chunk][great_ai.utilities.chunk.chunk].
    Useful for parallel processing.

    Similar to itertools.chain but ignores `None` chunks.

    Examples:
        >>> list(unchunk([[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]))
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    Args:
        chunks: Stream of chunks to unpack.

    Yields:
        The next item in the flattened iterable.
    """

    for chunk in chunks:
        if chunk is not None:
            yield from chunk
