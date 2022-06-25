from typing import Any, Callable

from ..context import get_context
from .get_function_metadata_store import get_function_metadata_store


def assert_function_is_not_finalised(func: Callable[..., Any]) -> None:
    error_message = (
        "The outer-most (first) decorator has to be `@GreatAI.deploy`. "
        + f"In the case of `{func.__name__}`, it is not: fix this by moving `@GreatAI.deploy` to the top."
    )

    if get_function_metadata_store(func).is_finalised:
        get_context().logger.error(error_message)
        exit(-1)
