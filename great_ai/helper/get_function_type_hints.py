import inspect
from typing import Any, Callable, Dict, get_type_hints


def get_function_type_hints(func: Callable) -> Dict[str, Any]:
    """Resolve postponed annotations in the original function's namespace."""
    return get_type_hints(inspect.unwrap(func), include_extras=True)
