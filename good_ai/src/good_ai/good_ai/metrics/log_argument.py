from functools import wraps
from typing import Any, Callable, Dict, List, Optional, Type

from ..exceptions import ArgumentValidationError
from ..helper import get_args
from ..tracing import TracingContext


def log_argument(
    argument_name: str,
    *,
    expected_type: Optional[Type] = None,
    validator: Callable[[Any], bool] = lambda _: True,
) -> Callable[..., Any]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        actual_name = f"{func.__name__}:{argument_name}"

        @wraps(func)
        def wrapper(*args: List[Any], **kwargs: Dict[str, Any]) -> Any:
            arguments = get_args(func, args, kwargs)
            argument = arguments[argument_name]

            if (
                expected_type is not None and not isinstance(argument, expected_type)
            ) or not validator(argument):
                raise ArgumentValidationError(
                    f"Argument {argument_name} in {func.__name__} did not pass validation"
                )

            context = TracingContext.get_current_context()
            if context:
                context.log_value(name=actual_name, value=argument)
            return func(*args, **kwargs)

        return wrapper

    return decorator
