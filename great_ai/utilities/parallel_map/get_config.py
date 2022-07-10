import os
from math import ceil
from typing import Callable, Iterable, Optional, Sequence, Union

from ..logger.get_logger import get_logger
from .parallel_map_configuration import ParallelMapConfiguration

logger = get_logger("parallel_map")


def get_config(
    *,
    function: Callable,
    input_values: Union[Sequence, Iterable],
    chunk_size: Optional[int],
    concurrency: Optional[int],
) -> ParallelMapConfiguration:

    is_input_sequence = hasattr(input_values, "__len__")
    input_length = len(input_values) if is_input_sequence else None  # type: ignore

    if concurrency is None:
        concurrency = os.cpu_count() or 1
    assert concurrency >= 1, "At least one mapper process has to be created"

    if chunk_size is None:
        if input_length is not None:
            chunk_size = max(1, ceil(input_length / concurrency / 10))
        else:
            raise ValueError(
                "The argument for `values` does not implement `__len__`, therefore, you must provide a `chunk_size`"
            )
    assert chunk_size >= 1, "Chunks have to contain at least one element"

    chunk_count: Optional[int] = None
    if input_length is not None:
        chunk_count = ceil(input_length / chunk_size)
        if chunk_count < concurrency:
            logger.warning(
                f"Limiting concurrency to {chunk_count} because there are only {chunk_count} chunks"
            )
            concurrency = chunk_count

    config = ParallelMapConfiguration(
        concurrency=concurrency,
        chunk_count=chunk_count,
        chunk_size=chunk_size,
        input_length=input_length,
        function_name=function.__name__ if hasattr(function, "__name__") else "unknown",
    )

    return config
