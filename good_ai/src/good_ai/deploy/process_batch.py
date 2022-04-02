from functools import partial, reduce
from typing import Any, Callable, Iterable, Optional, Sequence

from sus.parallel_map import parallel_map

from ..core import function_registry


def process_batch(
    function: Callable[..., Any],
    batch: Iterable[Any],
    concurrency: Optional[int] = None,
) -> Sequence[Any]:
    plugins = function_registry.get_plugins(function)
    composed = partial(reduce, lambda r, f: f(r), plugins)
    return parallel_map(composed, batch, concurrency=concurrency)
