import inspect
from typing import Any, Callable, Dict, Mapping, Sequence


def get_args(
    func: Callable[..., Any], args: Sequence[Any], kwargs: Mapping[str, Any]
) -> Dict[str, Any]:
    signature = inspect.signature(func)
    filter_keys = [
        param.name
        for param in signature.parameters.values()
        if param.kind == param.POSITIONAL_OR_KEYWORD
    ]
    return {**dict(zip(filter_keys, args)), **kwargs}
