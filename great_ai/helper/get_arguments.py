import inspect
from typing import Any, Callable, Dict, Mapping, Sequence


def get_arguments(
    func: Callable, args: Sequence[Any], kwargs: Mapping[str, Any]
) -> Dict[str, Any]:
    """Return mapping from parameter names to actual argument values."""

    signature = inspect.signature(func)

    defaults = {
        p.name: p.default
        for p in signature.parameters.values()
        if p.default != inspect._empty
    }

    filter_keys = [
        param.name
        for param in signature.parameters.values()
        if param.kind == param.POSITIONAL_OR_KEYWORD
    ]

    return {**defaults, **dict(zip(filter_keys, args)), **kwargs}
