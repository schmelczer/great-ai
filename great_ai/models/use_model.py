from functools import wraps
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, TypeVar, Union, cast

from dill import load
from typing_extensions import Literal  # <= Python 3.7

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
    """Inject a model into a function.

    Load a model specified by `key` and `version` using the currently active `LargeFile`
    implementation. If it's a single object, it is deserialised using `dill`. If it's a
    directory of files, a `pathlib.Path` instance is given.

    By default, the function's `model` parameter is replaced by the loaded model. This
    can be customised by changing `model_kwarg_name`. Multiple models can be loaded by
    decorating the same function with `use_model` multiple times.

    Examples:
            >>> from great_ai import save_model
            >>> save_model(3, 'my_number')
            'my_number:...'
            >>> @use_model('my_number')
            ... def my_function(a, model):
            ...     return a + model
            >>> my_function(4)
            7

    Args:
        key: The model's name as stored by the LargeFile implementation.
        version: The model's version as stored by the LargeFile implementation.
        model_kwarg_name: the parameter to use for injecting the loaded model
    Returns:
        A decorator for model injection.
    """

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
