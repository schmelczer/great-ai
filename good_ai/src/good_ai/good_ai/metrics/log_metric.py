import inspect
from typing import Any

from ..tracing import TracingContext


def log_metric(argument_name: str, value: Any) -> None:
    context = TracingContext.get_current_context()
    caller = inspect.stack()[1].function
    actual_name = f"metric:{caller}:{argument_name}"
    if context:
        context.log_value(name=actual_name, value=value)
