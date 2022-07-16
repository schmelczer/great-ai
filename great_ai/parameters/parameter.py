from functools import wraps
from typing import Any, Callable, Dict, TypeVar, cast

from typeguard import check_type

from ..errors import ArgumentValidationError
from ..helper import get_arguments, get_function_metadata_store
from ..helper.assert_function_is_not_finalised import assert_function_is_not_finalised
from ..tracing.tracing_context import TracingContext

F = TypeVar("F", bound=Callable)


def parameter(
    parameter_name: str,
    *,
    validate: Callable[[Any], bool] = lambda _: True,
    disable_logging: bool = False,
) -> Callable[[F], F]:
    """Control the validation and logging of function parameters.

    Basically, a parameter decorator. Unfortunately, Python does not have that concept,
    thus, it's a method decorator that expects the name of the to-be-decorated
    parameter.

    Examples:
        >>> @parameter('a')
        ... def my_function(a: int):
        ...     return a + 2
        >>> my_function(4)
        6
        >>> my_function('3')
        Traceback (most recent call last):
            ...
        TypeError: type of a must be int; got str instead

        >>> @parameter('positive_a', validate=lambda v: v > 0)
        ... def my_function(positive_a: int):
        ...     return a + 2
        >>> my_function(-1)
        Traceback (most recent call last):
            ...
        great_ai.errors.argument_validation_error.ArgumentValidationError: ...

    Args:
        parameter_name: Name of parameter to consider.
        validate: Optional validate to run against the concrete argument.
            ArgumentValidationError is thrown when the return value is False.
        disable_logging: Do not save the value in any active TracingContext.
    Returns:
        A decorator for argument validation.
    """

    def decorator(func: F) -> F:
        get_function_metadata_store(func).input_parameter_names.append(parameter_name)
        assert_function_is_not_finalised(func)

        actual_name = f"arg:{parameter_name}"

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Dict[str, Any]) -> Any:
            arguments = get_arguments(func, args, kwargs)
            argument = arguments.get(parameter_name)

            expected_type = func.__annotations__.get(parameter_name)

            if expected_type is not None:
                check_type(parameter_name, argument, expected_type)

            if not validate(argument):
                raise ArgumentValidationError(
                    f"""Argument {parameter_name} in {
                        func.__name__
                    } did not pass validation"""
                )

            context = TracingContext.get_current_tracing_context()
            if context and not disable_logging:
                context.log_value(name=f"{actual_name}:value", value=argument)
                if isinstance(argument, str):
                    context.log_value(name=f"{actual_name}:length", value=len(argument))

            return func(*args, **kwargs)

        return cast(F, wrapper)

    return decorator
