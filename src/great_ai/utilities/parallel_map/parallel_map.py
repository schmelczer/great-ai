import multiprocessing as mp
import queue
from typing import Callable, Dict, Iterable, Optional, Sequence, TypeVar, overload

from tqdm.cli import tqdm

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
    chunk_size: Optional[int],
    concurrency: Optional[int],
    disable_logging: bool,
    unordered: Optional[bool],
) -> Iterable[V]:
    ...


@overload
def parallel_map(
    function: Callable[[T], V],
    input_values: Iterable[T],
    *,
    chunk_size: int,
    concurrency: Optional[int],
    disable_logging: bool,
    unordered: Optional[bool],
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
        yield from (function(v) for v in tqdm(input_values, **tqdm_options))
        return

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

    progress = tqdm(**tqdm_options)

    chunks = iter(chunk(enumerate(input_values), chunk_size=config.chunk_size))
    indexed_results: Dict[int, V] = {}
    next_output_index = 0
    read_input_length = 0
    is_iteration_over = False
    try:
        while not is_iteration_over or next_output_index < read_input_length:
            if not is_iteration_over:
                try:
                    next_chunk = next(chunks)
                    input_queue.put(next_chunk)
                    read_input_length += len(next_chunk)
                except StopIteration:
                    is_iteration_over = True

            try:
                result_chunk = output_queue.get_nowait()
                progress.update(len(result_chunk))

                for index, value in result_chunk:
                    if unordered:
                        yield value
                        next_output_index += 1
                    else:
                        indexed_results[index] = value

                if not unordered:
                    while next_output_index in indexed_results:
                        yield indexed_results[next_output_index]
                        del indexed_results[next_output_index]
                        next_output_index += 1
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
