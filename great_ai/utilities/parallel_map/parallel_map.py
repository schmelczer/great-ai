import multiprocessing as mp
from typing import (
    Awaitable,
    Callable,
    Iterable,
    Optional,
    Sequence,
    TypeVar,
    Union,
    overload,
)

import dill
from typing_extensions import Literal  # <= Python 3.7

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
    """Execute a map operation on an iterable stream.

    A custom parallel map operation supporting both synchronous and `async` map
    functions. The `func` function is serialised with `dill`. Exceptions encountered in
    the map function are sent to the host process where they are either raised (default)
    or ignored.

    The new processes are forked if the OS allows it, otherwise, new Python processes
    are bootstrapped which can incur some start-up cost. Each process processes a single
    chunk at once.

    Examples:
        >>> import math
        >>> list(parallel_map(math.sqrt, [9, 4, 1], concurrency=2))
        [3.0, 2.0, 1.0]

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
        concurrency: Number of new processes to start. Shouldn't be too much more than
            the number of physical cores.
        unordered: Do not preserve the order of the elements, yield them as soon as they
            have been processed. This decreases the latency caused by
            difficult-to-process items.

    Yields:
        The next result obtained from applying `func` to each input value. May
            contain `None`-s if `ignore_exceptions=True`. May have different order than
            the input if `unordered=True`.

    Raises:
        WorkerException: If there was an error in the `func` function in a background
            process and `ignore_exceptions=False`.
    """

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
        ctx.Process(  # type: ignore
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
