import inspect
from typing import Any, Callable, Dict


def filter_args(
    dict_to_filter: Dict[str, Any], func: Callable[..., Any]
) -> Dict[str, Any]:
    signature = inspect.signature(func)
    filter_keys = [
        param.name
        for param in signature.parameters.values()
        if param.kind == param.POSITIONAL_OR_KEYWORD
    ]
    filtered_dict = {
        filter_key: dict_to_filter[filter_key] for filter_key in filter_keys
    }
    return filtered_dict
