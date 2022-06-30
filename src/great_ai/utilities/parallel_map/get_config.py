import os
from math import ceil
from typing import Callable, Iterable, Optional, Sequence, Union

import dill

from ..logger import get_logger
from .parallel_map_configuration import ParallelMapConfiguration

logger = get_logger("parallel_map")


def get_config(
    *,
    function: Callable,
    input_values: Union[Sequence, Iterable],
    chunk_size: Optional[int],
    concurrency: Optional[int],
    disable_logging: bool,
) -> ParallelMapConfiguration:

    is_input_sequence = hasattr(input_values, "__len__")

    if concurrency is None:
        concurrency = len(os.sched_getaffinity(0))
    assert concurrency >= 1, "At least one mapper process has to be created"

    if chunk_size is None:
        if is_input_sequence:
            chunk_size = max(1, ceil(len(input_values) / concurrency / 10))
        else:
            raise ValueError(
                "The argument for `values` does not implement `__len__`, therefore, you must provide a `chunk_size`"
            )
    assert chunk_size >= 1, "Chunks have to contain at least one element"

    chunk_count: Optional[int] = None
    if is_input_sequence:
        chunk_count = ceil(len(input_values) / chunk_size)
        if chunk_count < concurrency:
            logger.warning(
                f"Limiting concurrency to {chunk_count} because there are only {chunk_count} chunks"
            )
            concurrency = chunk_count

    if concurrency == 1:
        logger.warning("Running in series, there is no reason for parallelism")

    input_length = len(input_values) if is_input_sequence else None

    config = ParallelMapConfiguration(
        concurrency=concurrency,
        chunk_count=chunk_count,
        chunk_size=chunk_size,
        input_length=input_length,
        serialized_map_function=dill.dumps(function, byref=True, recurse=True),
        function_name=function.__name__,
    )

    if not disable_logging:
        logger.info("Parallel map: configured ✅")
        config.pretty_print()

    return config
