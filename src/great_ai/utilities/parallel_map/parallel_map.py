import multiprocessing as mp
from typing import Callable, Iterable, Optional, Sequence, TypeVar, overload

from src.great_ai.utilities.parallel_map.manage_communication import (
    manage_communication,
)

from .get_config import get_config
from .manage_serial import manage_serial
from .mapper_function import mapper_function

T = TypeVar("T")
V = TypeVar("V")


@overload
def parallel_map(
    function: Callable[[T], V],
    input_values: Sequence[T],
    *,
    chunk_size: Optional[int],
    concurrency: Optional[int],
    disable_logging: Optional[bool],
    unordered: Optional[bool],
    ignore_exceptions: Optional[bool],
) -> Iterable[V]:
    ...


@overload
def parallel_map(
    function: Callable[[T], V],
    input_values: Iterable[T],
    *,
    chunk_size: int,
    concurrency: Optional[int],
    disable_logging: Optional[bool],
    unordered: Optional[bool],
    ignore_exceptions: Optional[bool],
) -> Iterable[V]:
    ...


def parallel_map(
    function,
    input_values,
    *,
    chunk_size=None,
    concurrency=None,
    disable_logging=False,
    unordered=False,
    ignore_exceptions=False,
):
    config = get_config(
        function=function,
        input_values=input_values,
        chunk_size=chunk_size,
        concurrency=concurrency,
        disable_logging=disable_logging,
    )

    tqdm_options = dict(
        desc=f"Parallel map {config.function_name}",
        disable=disable_logging,
        total=config.input_length,
        miniters=1,
        dynamic_ncols=True,
    )

    if config.concurrency == 1:
        yield from manage_serial(
            function=function,
            tqdm_options=tqdm_options,
            input_values=input_values,
            ignore_exceptions=ignore_exceptions,
        )

    ctx = mp.get_context("spawn")
    ctx.freeze_support()

    input_queue = ctx.Queue(0 if config.chunk_count is None else config.chunk_count)
    output_queue = ctx.Queue(0 if config.chunk_count is None else config.chunk_count)
    should_stop = ctx.Event()

    processes = [
        ctx.Process(
            name=f"parallel_map_{config.function_name}_{i}",
            target=mapper_function,
            kwargs=dict(
                input_queue=input_queue,
                output_queue=output_queue,
                should_stop=should_stop,
                serialized_map_function=config.serialized_map_function,
            ),
        )
        for i in range(config.concurrency)
    ]

    for p in processes:
        p.start()

    try:
        yield from manage_communication(
            tqdm_options=tqdm_options,
            input_values=input_values,
            chunk_size=config.chunk_size,
            input_queue=input_queue,
            output_queue=output_queue,
            unordered=unordered,
            ignore_exceptions=ignore_exceptions,
        )
    finally:
        should_stop.set()
        for p in processes:
            p.join()
            p.close()
        input_queue.close()
        output_queue.close()
