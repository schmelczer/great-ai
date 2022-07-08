from typing import Callable

from ..errors import WrongDecoratorOrderError
from .get_function_metadata_store import get_function_metadata_store


def assert_function_is_not_finalised(func: Callable) -> None:
    error_message = (
        "The outer-most (first) decorator has to be `@GreatAI.deploy`. "
        + f"In the case of `{func.__name__}`, it is not: fix this by moving `@GreatAI.deploy` to the top."
    )

    if get_function_metadata_store(func).is_finalised:
        raise WrongDecoratorOrderError(error_message)
