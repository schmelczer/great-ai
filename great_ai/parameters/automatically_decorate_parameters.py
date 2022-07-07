import inspect
from typing import Callable, TypeVar

from ..helper.get_function_metadata_store import get_function_metadata_store
from .parameter import parameter

F = TypeVar("F", bound=Callable)


def automatically_decorate_parameters(func: F) -> F:
    signature = inspect.signature(func)
    parameter_names = [
        param.name
        for param in signature.parameters.values()
        if param.kind == param.POSITIONAL_OR_KEYWORD
    ]

    metadata = get_function_metadata_store(func)

    for name in parameter_names:
        if (
            name not in metadata.model_parameter_names
            and name not in metadata.input_parameter_names
        ):
            func = parameter(name)(func)

    return func
