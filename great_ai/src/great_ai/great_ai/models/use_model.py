from functools import wraps
from typing import Any, Callable, Dict, List, Literal, Union

from ..helper import get_function_metadata_store
from ..tracing import TracingContext
from ..views import Model
from .load_model import load_model


def use_model(
    key: str,
    *,
    version: Union[int, Literal["latest"]],
    return_path: bool = False,
    model_kwarg_name: str = "model",
) -> Callable[..., Any]:
    assert isinstance(version, int) or version == "latest"

    model, actual_version = load_model(
        key=key,
        version=None if version == "latest" else version,
        return_path=return_path,
    )

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        store = get_function_metadata_store(func)
        store.model_parameter_names.append(model_kwarg_name)
        if store.version:
            store.version += "|"
        store.version += f"{key}:{actual_version}"

        @wraps(func)
        def wrapper(*args: List[Any], **kwargs: Dict[str, Any]) -> Any:
            context = TracingContext.get_current_context()
            if context:
                context.log_model(Model(key=key, version=actual_version))
            return func(*args, **kwargs, **{model_kwarg_name: model})

        return wrapper

    return decorator
