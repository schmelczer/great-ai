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
