from typing import Any, Callable, cast

from ..views.function_metadata import FunctionMetadata


def get_function_metadata_store(func: Callable[..., Any]) -> FunctionMetadata:
    any_func = cast(Any, func)

    if not hasattr(any_func, "_great_ai_metadata"):
        any_func._great_ai_metadata = FunctionMetadata()

    return any_func._great_ai_metadata
