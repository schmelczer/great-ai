from functools import wraps
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Literal,
    Optional,
    Set,
    Tuple,
    TypeVar,
    Union,
    cast,
)

from dill import load

from ..context import get_context
from ..helper import get_function_metadata_store
from ..helper.assert_function_is_not_finalised import assert_function_is_not_finalised
from ..tracing.tracing_context import TracingContext
from ..views import Model

F = TypeVar("F", bound=Callable)


def use_model(
    key: str,
    *,
    version: Union[int, Literal["latest"]] = "latest",
    model_kwarg_name: str = "model",
) -> Callable[[F], F]:
    assert (
        isinstance(version, int) or version == "latest"
    ), "Only integers or the string literal `latest` is allowed as a version"

    model, actual_version = _load_model(
        key=key,
        version=None if version == "latest" else version,
    )

    def decorator(func: F) -> F:
        assert_function_is_not_finalised(func)

        store = get_function_metadata_store(func)
        store.model_parameter_names.append(model_kwarg_name)

        @wraps(func)
        def wrapper(*args: List[Any], **kwargs: Dict[str, Any]) -> Any:
            tracing_context = TracingContext.get_current_tracing_context()
            if tracing_context:
                tracing_context.log_model(Model(key=key, version=actual_version))
            return func(*args, **kwargs, **{model_kwarg_name: model})

        return cast(F, wrapper)

    return decorator


model_versions: Set[Tuple[str, int]] = set()


def _load_model(key: str, version: Optional[int] = None) -> Tuple[Any, int]:
    file = get_context().large_file_implementation(name=key, mode="rb", version=version)
    path = file.get()

    model_versions.add((key, file.version))

    if path.is_dir():
        return path, file.version

    with file as f:
        loaded = load(f)

    return loaded, file.version
