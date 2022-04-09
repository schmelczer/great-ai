from functools import wraps
from typing import Any, Callable, Dict, List

from ..helper import filter_args, get_args
from ..tracing import TracingContext


def log_metric(
    argument_name: str, *, calculate: Callable[[Any], bool] = lambda _: True
) -> Callable[..., Any]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        actual_name = f"{func.__name__}:{argument_name}"

        @wraps(func)
        def wrapper(*args: List[Any], **kwargs: Dict[str, Any]) -> Any:
            arguments = get_args(func, args, kwargs)
            metric = calculate(**filter_args(arguments, calculate))

            context = TracingContext.get_current_context()
            if context:
                context.log_value(name=actual_name, value=metric)
            return func(*args, **kwargs)

        return wrapper

    return decorator
