import multiprocessing as mp
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

import dill

from .get_config import get_config
from .manage_communication import manage_communication
from .mapper_function import mapper_function
from .worker_exception import WorkerException

T = TypeVar("T")
V = TypeVar("V")


@overload
def parallel_map(
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
def parallel_map(
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
def parallel_map(
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
def parallel_map(
    func: Callable[[T], Union[V, Awaitable[V]]],
    input_values: Union[Iterable[T], Sequence[T]],
    *,
    chunk_size: int,
    ignore_exceptions: Literal[False] = ...,
    concurrency: Optional[int] = ...,
    unordered: bool = ...,
) -> Iterable[V]:
    ...


def parallel_map(
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

    ctx = (
        mp.get_context("fork")
        if "fork" in mp.get_all_start_methods()
        else mp.get_context("spawn")
    )
    ctx.freeze_support()
    manager = ctx.Manager()
    input_queue = manager.Queue(config.concurrency * 2)
    output_queue = manager.Queue(config.concurrency * 2)

    should_stop = ctx.Event()
    serialized_map_function = dill.dumps(func, byref=True, recurse=False)

    processes = [
        ctx.Process(
            name=f"parallel_map_{config.function_name}_{i}",
            target=mapper_function,
            daemon=True,
            kwargs=dict(
                input_queue=input_queue,
                output_queue=output_queue,
                should_stop=should_stop,
                func=serialized_map_function,
            ),
        )
        for i in range(config.concurrency)
    ]

    for p in processes:
        p.start()

    try:
        yield from manage_communication(
            input_values=input_values,
            chunk_size=config.chunk_size,
            input_queue=input_queue,
            output_queue=output_queue,
            unordered=unordered,
            ignore_exceptions=ignore_exceptions,
        )
        should_stop.set()
    except WorkerException:
        should_stop.set()
        raise
    except Exception:
        for p in processes:
            p.terminate()
            p.kill()
        raise
    finally:
        for p in processes:
            p.join()  # terminated processes have to be joined else they remain zombies
            p.close()

        manager.shutdown()
