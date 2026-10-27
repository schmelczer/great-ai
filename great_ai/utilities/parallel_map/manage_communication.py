import multiprocessing as mp
import queue
import traceback
from typing import Callable, Dict, Iterable, List, Optional, Tuple, TypeVar, Union

from ..chunk import chunk
from ..logger.get_logger import get_logger
from .map_result import MapResult
from .worker_exception import WorkerException

logger = get_logger("parallel_map")

T = TypeVar("T")
V = TypeVar("V")


def manage_communication(
    *,
    input_values: Iterable[T],
    chunk_size: int,
    input_queue: Union[mp.Queue, queue.Queue],
    output_queue: Union[mp.Queue, queue.Queue],
    unordered: bool,
    ignore_exceptions: bool,
    check_workers: Optional[Callable[[], None]] = None,
) -> Iterable[V]:
    chunks = iter(chunk(enumerate(input_values), chunk_size=chunk_size))
    indexed_results: Dict[int, V] = {}
    next_output_index = 0
    read_input_length = 0
    is_iteration_over = False
    pending_chunk: Optional[List[Tuple[int, T]]] = None

    while not is_iteration_over or next_output_index < read_input_length:
        if check_workers is not None:
            check_workers()
        if not is_iteration_over:
            try:
                if pending_chunk is None:
                    pending_chunk = next(chunks)
                input_queue.put(pending_chunk, timeout=0.1)
                read_input_length += len(pending_chunk)
                pending_chunk = None
            except queue.Full:
                pass  # Retry the same chunk after checking worker health.
            except StopIteration:
                is_iteration_over = True
            except Exception as e:
                if ignore_exceptions:
                    logger.error(f"""Exception {e} encountered in input, traceback:\n{
                            traceback.format_exc()
                        }""")
                else:
                    raise

        try:
            result_chunk: List[MapResult] = output_queue.get(timeout=0.01)
            for r in result_chunk:
                if r.exception is not None:
                    if ignore_exceptions:
                        logger.error(
                            f"""Exception {
                                r.exception
                            } encountered in worker, traceback:\n{r.worker_traceback}"""
                        )
                    else:
                        raise WorkerException(r.exception)

                if unordered:

                    yield r.value
                    next_output_index += 1
                else:
                    indexed_results[r.order] = r.value

            if not unordered:
                while next_output_index in indexed_results:
                    yield indexed_results[next_output_index]
                    del indexed_results[next_output_index]
                    next_output_index += 1
        except queue.Empty:
            pass
