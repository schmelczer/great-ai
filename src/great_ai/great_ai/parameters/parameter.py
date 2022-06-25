from functools import wraps
from typing import Any, Callable, Dict, TypeVar, cast

from ..exceptions import ArgumentValidationError
from ..helper import get_arguments, get_function_metadata_store
from ..helper.assert_function_is_not_finalised import assert_function_is_not_finalised
from ..tracing.tracing_context import TracingContext

F = TypeVar("F", bound=Callable[..., Any])


def parameter(
    parameter_name: str,
    *,
    validator: Callable[[Any], bool] = lambda _: True,
    disable_logging: bool = False,
) -> Callable[[F], F]:
    def decorator(func: F) -> F:
        get_function_metadata_store(func).input_parameter_names.append(parameter_name)
        assert_function_is_not_finalised(func)

        actual_name = f"arg:{parameter_name}"

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

            context = TracingContext.get_current_tracing_context()
            if context and not disable_logging:
                context.log_value(name=f"{actual_name}:value", value=argument)
                if isinstance(argument, str):
                    context.log_value(name=f"{actual_name}:length", value=len(argument))

            return func(*args, **kwargs)

        return cast(F, wrapper)

    return decorator