import queue
import threading
from typing import Callable, Iterable, Literal, Optional, Sequence, TypeVar, overload

from .get_config import get_config
from .manage_communication import manage_communication
from .manage_serial import manage_serial
from .mapper_function import mapper_function

T = TypeVar("T")
V = TypeVar("V")


@overload
def threaded_parallel_map(
    function: Callable[[T], V],
    input_values: Sequence[T],
    *,
    chunk_size: Optional[int],
    concurrency: Optional[int],
    unordered: Optional[bool],
    ignore_exceptions: Optional[Literal[False]],
) -> Iterable[V]:
    ...


@overload
def threaded_parallel_map(
    function: Callable[[T], V],
    input_values: Iterable[T],
    *,
    chunk_size: int,
    concurrency: Optional[int],
    unordered: Optional[bool],
    ignore_exceptions: Optional[Literal[False]],
) -> Iterable[V]:
    ...


@overload
def threaded_parallel_map(
    function: Callable[[T], V],
    input_values: Sequence[T],
    *,
    chunk_size: Optional[int],
    concurrency: Optional[int],
    unordered: Optional[bool],
    ignore_exceptions: True,
) -> Iterable[Optional[V]]:
    ...


@overload
def threaded_parallel_map(
    function: Callable[[T], V],
    input_values: Iterable[T],
    *,
    chunk_size: int,
    concurrency: Optional[int],
    unordered: Optional[bool],
    ignore_exceptions: True,
) -> Iterable[Optional[V]]:
    ...


def threaded_parallel_map(
    function,
    input_values,
    *,
    chunk_size=None,
    concurrency=None,
    unordered=False,
    ignore_exceptions=False,
):
    config = get_config(
        function=function,
        input_values=input_values,
        chunk_size=chunk_size,
        concurrency=concurrency,
    )

    if config.concurrency == 1:
        yield from manage_serial(
            function=function,
            input_values=input_values,
            ignore_exceptions=ignore_exceptions,
        )

    input_queue = queue.Queue(config.concurrency * 2)
    output_queue = queue.Queue(config.concurrency * 2)
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
                serialized_map_function=config.serialized_map_function,
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
        t.join()
