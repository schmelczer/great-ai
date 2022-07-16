import inspect
from typing import Any

from ..context import get_context
from ..tracing import TracingContext


def log_metric(argument_name: str, value: Any) -> None:
    """Log a key (argument_name)-value pair that is persisted inside the trace.

    The name of the function from where this is called is also stored.

    Args:
        argument_name: The key for storing the value.
        value: Value to log. Must be JSON-serialisable.
    """

    tracing_context = TracingContext.get_current_tracing_context()
    caller = inspect.stack()[1].function
    actual_name = f"metric:{caller}:{argument_name}"
    if tracing_context:
        tracing_context.log_value(name=actual_name, value=value)

    get_context().logger.info(f"{actual_name}={value}")
