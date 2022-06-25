from math import ceil
from typing import Any, Callable, Iterable, List, Optional

import multiprocess as mp
from tqdm.cli import tqdm

from .logger import get_logger

logger = get_logger("parallel_map")


def parallel_map(
    function: Callable[[Any], Any],
    values: Iterable[Any],
    chunk_size: Optional[int] = None,
    concurrency: Optional[int] = None,
    disable_progress: bool = False,
) -> List[Any]:
    if concurrency is None:
        concurrency = mp.cpu_count()

    assert concurrency > 0
    assert chunk_size is None or chunk_size > 0

    values = list(values)

    if not chunk_size:
        chunk_size = max(1, ceil(len(values) / concurrency / 10))

    chunk_count = ceil(len(values) / chunk_size)
    if chunk_count < concurrency:
        logger.warning(
            f"Limiting concurrency to {chunk_count} because there are only {chunk_count} chunks"
        )
        concurrency = chunk_count

    logger.info(
        f"Starting parallel map (concurrency: {concurrency}, chunk size: {chunk_size})"
    )

    if concurrency == 1 or len(values) <= chunk_size:
        logger.warning("Running in series, there is no reason for parallelism")
        iterable = values if disable_progress else tqdm(values)
        return [function(v) for v in iterable]

    with mp.Pool(processes=concurrency) as pool:
        if disable_progress:
            return pool.map(function, values, chunksize=chunk_size)

        return list(
            tqdm(pool.imap(function, values, chunksize=chunk_size), total=len(values))
        )
