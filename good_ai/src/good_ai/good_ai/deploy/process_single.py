from typing import Any, Callable

from ..tracing import TracingContext
from ..views import Trace


def process_single(function: Callable[..., Any], input_value: Any) -> Trace:
    with TracingContext() as t:
        t.log_input(input_value)
        result = function(input_value)
        output = t.log_output(result)
    return output
