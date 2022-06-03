from functools import wraps
from typing import Any, Callable, Dict

from ..exceptions import ArgumentValidationError
from ..helper import (
    assert_function_is_not_finalised,
    get_arguments,
    get_function_metadata_store,
)
from ..tracing.tracing_context import TracingContext


def parameter(
    parameter_name: str,
    *,
    validator: Callable[[Any], bool] = lambda _: True,
    disable_logging: bool = False,
) -> Callable[..., Any]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        get_function_metadata_store(func).input_parameter_names.append(parameter_name)
        assert_function_is_not_finalised(func)

        actual_name = f"arg:{func.__name__}:{parameter_name}"

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Dict[str, Any]) -> Any:
            arguments = get_arguments(func, args, kwargs)
            argument = arguments[parameter_name]

            expected_type = func.__annotations__.get(parameter_name)

            if expected_type is not None and not isinstance(argument, expected_type):
                raise ArgumentValidationError(
                    f"Argument {parameter_name} in {func.__name__} has the wrong type, expected: {expected_type.__name__}, got: {type(argument).__name__}"
                )

            if not validator(argument):
                raise ArgumentValidationError(
                    f"Argument {parameter_name} in {func.__name__} did not pass validation"
                )

            context = TracingContext.get_current_context()
            if context and not disable_logging:
                context.log_value(name=actual_name, value=argument)
                if isinstance(argument, str):
                    context.log_value(name=f"{actual_name}:length", value=len(argument))

            return func(*args, **kwargs)

        return wrapper

    return decorator
