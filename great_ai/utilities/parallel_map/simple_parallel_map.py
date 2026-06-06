from typing import Awaitable, Callable, List, Optional, Sequence, TypeVar, Union

from tqdm import tqdm

from .parallel_map import parallel_map

T = TypeVar("T")
V = TypeVar("V")


def simple_parallel_map(
    func: Callable[[T], Union[V, Awaitable[V]]],
    input_values: Sequence[T],
    *,
    chunk_size: Optional[int] = None,
    concurrency: Optional[int] = None,
) -> List[V]:
    """Execute a map operation on an list mimicking the API of the built-in `map()`.

    A thin-wrapper over [parallel_map][great_ai.utilities.parallel_map.parallel_map.parallel_map].
    For more options, consult the documentation of
    [parallel_map][great_ai.utilities.parallel_map.parallel_map.parallel_map].

    Examples:
        >>> import math
        >>> list(simple_parallel_map(math.sqrt, [9, 4, 1]))
        [3.0, 2.0, 1.0]

    Args:
        func: The function that should be applied to each element of `input_values`.
            It can `async`, in that case, a new event loop is started for each chunk.
        input_values: An iterable of items that `func` is applied to.
        chunk_size: Tune the number of items processed in each step. Larger numbers
            result in smaller communication overhead but less parallelism at the start
            and end. If `chunk_size` has a `__len__` property, the `chunk_size` is
            calculated automatically if not given.
        concurrency: Number of new processes to start. Shouldn't be too much more than
            the number of physical cores.

    Returns:
        An iterable of results obtained from applying `func` to each input value.

    Raises:
        WorkerException: If there was an error in the `func` function in a background
            process.
    """

    input_values = list(input_values)  # in case the input is mistakenly not a sequence
    generator = parallel_map(
        func=func,
        input_values=input_values,
        chunk_size=chunk_size,
        concurrency=concurrency,
    )

    return list(
        tqdm(
            generator,
            total=len(input_values),
        )
    )
