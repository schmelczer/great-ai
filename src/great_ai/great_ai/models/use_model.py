from functools import wraps
from typing import Any, Callable, Dict, List, Literal, TypeVar, Union, cast

from ..helper import get_function_metadata_store
from ..helper.assert_function_is_not_finalised import assert_function_is_not_finalised
from ..tracing.tracing_context import TracingContext
from ..views import Model
from .load_model import load_model

F = TypeVar("F", bound=Callable[..., Any])


def use_model(
    key: str,
    *,
    version: Union[int, Literal["latest"]],
    model_kwarg_name: str = "model",
) -> Callable[[F], F]:
    assert (
        isinstance(version, int) or version == "latest"
    ), "Only integers or the string literal `latest` is allowed as version"

    model, actual_version = load_model(
        key=key,
        version=None if version == "latest" else version,
    )

    def decorator(func: F) -> F:
        assert_function_is_not_finalised(func)

        store = get_function_metadata_store(func)
        store.model_parameter_names.append(model_kwarg_name)
        if store.model_versions:
            store.model_versions += "."
        store.model_versions += f"{key}-v{actual_version}"

        @wraps(func)
        def wrapper(*args: List[Any], **kwargs: Dict[str, Any]) -> Any:
            tracing_context = TracingContext.get_current_tracing_context()
            if tracing_context:
                tracing_context.log_model(Model(key=key, version=actual_version))
            return func(*args, **kwargs, **{model_kwarg_name: model})

        return cast(F, wrapper)

    return decorator
