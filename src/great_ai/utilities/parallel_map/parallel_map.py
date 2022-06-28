import multiprocessing as mp
import queue
from typing import (
    Callable,
    Iterable,
    List,
    Optional,
    Sequence,
    Tuple,
    TypeVar,
    overload,
)

from tqdm.auto import tqdm

from ..chunk import chunk
from .get_config import get_config
from .mapper_function import mapper_function

T = TypeVar("T")
V = TypeVar("V")


@overload
def parallel_map(
    function: Callable[[T], V],
    input_values: Sequence[T],
    *,
    chunk_length: Optional[int],
    concurrency: Optional[int],
    disable_progress_bar: bool,
) -> List[V]:
    ...


@overload
def parallel_map(
    function: Callable[[T], V],
    input_values: Iterable[T],
    *,
    chunk_length: int,
    concurrency: Optional[int],
    disable_progress_bar: bool,
) -> List[V]:
    ...


def parallel_map(
    function,
    input_values,
    *,
    chunk_length=None,
    concurrency=None,
    disable_progress_bar=False,
):
    config = get_config(
        function=function,
        input_values=input_values,
        chunk_length=chunk_length,
        concurrency=concurrency,
    )

    if config.concurrency == 1:
        return [
            function(v)
            for v in tqdm(
                input_values,
                desc="Parallel map",
                disable=disable_progress_bar,
                total=config.input_length,
                miniters=1,
            )
        ]

    ctx = mp.get_context("spawn")
    ctx.freeze_support()
    input_queue = ctx.Queue(0 if config.chunk_count is None else config.chunk_count)
    output_queue = ctx.Queue(0 if config.chunk_count is None else config.chunk_count)
    should_stop = ctx.Event()

    processes = [
        ctx.Process(
            name=f"parallel_map_{i}",
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

    progress = tqdm(
        desc="Parallel map",
        disable=disable_progress_bar,
        total=config.input_length,
        miniters=1,
    )

    chunks = iter(chunk(enumerate(input_values), chunk_length=config.chunk_length))
    indexed_results: List[Tuple[int, V]] = []
    read_input_length = 0
    is_iteration_over = False
    try:
        while not is_iteration_over or len(indexed_results) < read_input_length:
            if not is_iteration_over:
                try:
                    next_chunk = next(chunks)
                    input_queue.put(next_chunk)
                    read_input_length += len(next_chunk)
                except StopIteration:
                    is_iteration_over = True

            try:
                result_chunk = output_queue.get_nowait()
                indexed_results.extend(result_chunk)
                progress.update(len(result_chunk))
            except queue.Empty:
                pass
        should_stop.set()
    except KeyboardInterrupt:
        for p in processes:
            p.terminate()
    finally:
        for p in processes:
            p.join()
            p.close()
        input_queue.close()
        output_queue.close()

        progress.close()

    results = [v for _, v in sorted(indexed_results)]

    return results
