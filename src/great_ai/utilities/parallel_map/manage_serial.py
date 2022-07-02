import traceback
from typing import Callable, Iterable, TypeVar

from ..logger import get_logger

logger = get_logger("parallel_map")

T = TypeVar("T")
V = TypeVar("V")


def manage_serial(
    *,
    function: Callable[[T], V],
    input_values: Iterable[T],
    ignore_exceptions: bool,
) -> Iterable[V]:
    try:
        for v in input_values:
            try:
                yield function(v)
            except Exception as e:
                if not ignore_exceptions:
                    raise e
                else:
                    logger.error(
                        f"Exception {e} encountered in input, traceback:\n{traceback.format_exc()}"
                    )
    except Exception as e:
        if not ignore_exceptions:
            raise e
        else:
            logger.error(
                f"Exception {e} encountered in worker, traceback:\n{traceback.format_exc()}"
            )
