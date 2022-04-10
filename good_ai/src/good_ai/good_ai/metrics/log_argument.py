from functools import wraps
from typing import Any, Callable, Dict, List

from ..exceptions import ArgumentValidationError
from ..helper import get_args
from ..tracing import TracingContext


def log_argument(
    argument_name: str,
    *,
    validator: Callable[[Any], bool] = lambda _: True,
) -> Callable[..., Any]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        actual_name = f"arg:{func.__name__}:{argument_name}"

        @wraps(func)
        def wrapper(*args: List[Any], **kwargs: Dict[str, Any]) -> Any:
            arguments = get_args(func, args, kwargs)
            argument = arguments[argument_name]

            expected_type = func.__annotations__.get(argument_name)

            if (
                expected_type is not None and not isinstance(argument, expected_type)
            ):
                raise ArgumentValidationError(
                    f"Argument {argument_name} in {func.__name__} has the wrong type, expected: {expected_type.__name__}, got: {type(argument).__name__}"
                )

            if not validator(argument):
                raise ArgumentValidationError(
                    f"Argument {argument_name} in {func.__name__} did not pass validation"
                )

            context = TracingContext.get_current_context()
            if context:
                context.log_value(name=actual_name, value=argument)
            return func(*args, **kwargs)

        return wrapper

    return decorator
