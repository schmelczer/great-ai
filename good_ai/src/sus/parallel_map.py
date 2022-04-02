from math import ceil
from typing import Any, Callable, Iterable, List, Optional

import multiprocess as mp
import psutil
from tqdm.auto import tqdm


def parallel_map(
    function: Callable[[Any], Any],
    values: Iterable[Any],
    chunk_size: Optional[int] = None,
    concurrency: int = psutil.cpu_count(),
    disable_progress: bool = False,
) -> List[Any]:
    assert concurrency > 0
    assert chunk_size is None or chunk_size > 0

    values = list(values)

    if not chunk_size:
        chunk_size = max(1, ceil(len(values) / concurrency / 10))

    if concurrency == 1:
        iterable = values if disable_progress else tqdm(values)
        return [function(v) for v in iterable]

    with mp.Pool(processes=concurrency) as pool:
        if disable_progress:
            return pool.map(function, values, chunksize=chunk_size)

        return list(
            tqdm(pool.imap(function, values, chunksize=chunk_size), total=len(values))
        )
