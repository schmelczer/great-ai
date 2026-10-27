import inspect
from typing import Any, Callable, Dict, Mapping, Sequence


def get_arguments(
    func: Callable, args: Sequence[Any], kwargs: Mapping[str, Any]
) -> Dict[str, Any]:
    """Return mapping from parameter names to actual argument values."""

    signature = inspect.signature(func)

    # Model-injected parameters may not have been supplied at this wrapper layer.
    arguments = signature.bind_partial(*args, **kwargs)
    arguments.apply_defaults()
    return dict(arguments.arguments)
