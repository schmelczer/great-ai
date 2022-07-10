import queue
import threading
from typing import (
    Awaitable,
    Callable,
    Iterable,
    Literal,
    Optional,
    Sequence,
    TypeVar,
    Union,
    overload,
)

from .get_config import get_config
from .manage_communication import manage_communication
from .mapper_function import mapper_function

T = TypeVar("T")
V = TypeVar("V")


@overload
def threaded_parallel_map(
    func: Callable[[T], Union[V, Awaitable[V]]],
    input_values: Sequence[T],
    *,
    ignore_exceptions: Literal[True],
    chunk_size: Optional[int] = ...,
    concurrency: Optional[int] = ...,
    unordered: bool = ...,
) -> Iterable[Optional[V]]:
    ...


@overload
def threaded_parallel_map(
    func: Callable[[T], Union[V, Awaitable[V]]],
    input_values: Union[Iterable[T], Sequence[T]],
    *,
    chunk_size: int,
    ignore_exceptions: Literal[True],
    concurrency: Optional[int] = ...,
    unordered: bool = ...,
) -> Iterable[Optional[V]]:
    ...


@overload
def threaded_parallel_map(
    func: Callable[[T], Union[V, Awaitable[V]]],
    input_values: Sequence[T],
    *,
    chunk_size: Optional[int] = ...,
    ignore_exceptions: Literal[False] = ...,
    concurrency: Optional[int] = ...,
    unordered: bool = ...,
) -> Iterable[V]:
    ...


@overload
def threaded_parallel_map(
    func: Callable[[T], Union[V, Awaitable[V]]],
    input_values: Union[Iterable[T], Sequence[T]],
    *,
    chunk_size: int,
    ignore_exceptions: Literal[False] = ...,
    concurrency: Optional[int] = ...,
    unordered: bool = ...,
) -> Iterable[V]:
    ...


def threaded_parallel_map(
    func: Callable[[T], Union[V, Awaitable[V]]],
    input_values: Union[Iterable[T], Sequence[T]],
    *,
    chunk_size: Optional[int] = None,
    ignore_exceptions: bool = False,
    concurrency: Optional[int] = None,
    unordered: bool = False,
) -> Iterable[Optional[V]]:
    """Execute a map operation on an iterable stream.

    Similar to [parallel_map][great_ai.utilities.parallel_map.parallel_map.parallel_map]
    but uses threads instead of processes. Hence, it is not helpful in CPU-bound
    situations.

    A custom parallel map operation supporting both synchronous and `async` map
    functions. Exceptions encountered in the map function are sent to the host thread
    where they are either raised (default) or ignored. Each process processes a single
    chunk at once.

    Examples:
        >>> list(threaded_parallel_map(lambda x: x ** 2, [1, 2, 3]))
        [1, 4, 9]

    Args:
        func: The function that should be applied to each element of `input_values`.
            It can `async`, in that case, a new event loop is started for each chunk.
        input_values: An iterable of items that `func` is applied to.
        chunk_size: Tune the number of items processed in each step. Larger numbers
            result in smaller communication overhead but less parallelism at the start
            and end. If `chunk_size` has a `__len__` property, the `chunk_size` is
            calculated automatically if not given.
        ignore_exceptions: Ignore chunks if `next()` raises an exception on
            `input_values`. And return `None` if `func` raised an exception in a worker
            process.
        concurrency: Number of new threads to start.
        unordered: Do not preserve the order of the elements, yield them as soon as they
            have been processed. This decreases the latency caused by
            difficult-to-process items.

    Yields:
        The next result obtained from applying `func` to each input value. May
            contain `None`-s if `ignore_exceptions=True`. May have different order than
            the input if `unordered=True`.

    Raises:
        WorkerException: If there was an error in the `func` function in a background
            thread and `ignore_exceptions=False`.
    """

    config = get_config(
        function=func,
        input_values=input_values,
        chunk_size=chunk_size,
        concurrency=concurrency,
    )

    input_queue: queue.Queue = queue.Queue(config.concurrency * 2)
    output_queue: queue.Queue = queue.Queue(config.concurrency * 2)
    should_stop = threading.Event()

    threads = [
        threading.Thread(
            name=f"threaded_parallel_map_{config.function_name}_{i}",
            target=mapper_function,
            daemon=True,
            kwargs=dict(
                input_queue=input_queue,
                output_queue=output_queue,
                should_stop=should_stop,
                func=func,
            ),
        )
        for i in range(config.concurrency)
    ]

    for t in threads:
        t.start()

    yield from manage_communication(
        input_values=input_values,
        chunk_size=config.chunk_size,
        input_queue=input_queue,
        output_queue=output_queue,
        unordered=unordered,
        ignore_exceptions=ignore_exceptions,
    )
    should_stop.set()
    for t in threads:
        t.join(1)
