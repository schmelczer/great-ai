import inspect
from typing import Any, Callable, cast

from ..views.function_metadata import FunctionMetadata


def get_function_metadata_store(func: Callable) -> FunctionMetadata:
    any_func = cast(Any, func)

    if not hasattr(any_func, "_great_ai_metadata"):
        is_asynchronous = inspect.iscoroutinefunction(func)
        any_func._great_ai_metadata = FunctionMetadata(is_asynchronous=is_asynchronous)

    return any_func._great_ai_metadata
