from typing import Any, Callable, Iterable, Optional, Sequence

from good_ai.utilities.parallel_map import parallel_map

from ..context import get_context
from ..tracing import TracingContext
from ..views import Trace


def process_batch(
    function: Callable[..., Any],
    batch: Iterable[Any],
    concurrency: Optional[int] = None,
) -> Sequence[Trace]:
    def inner(input: Any) -> Trace:
        with TracingContext() as t:
            result = function(input)
            output = t.log_output(result)
        return output

    if not get_context().persistence.is_threadsafe:
        concurrency = 1
        get_context().logger.warn("Concurrency is ignored")

    return parallel_map(inner, batch, concurrency=concurrency)
