from pathlib import Path
from typing import Optional, Union

from dill import dump

from ..context import get_context


def save_model(
    model: Union[Path, str, object], key: str, *, keep_last_n: Optional[int] = None
) -> str:
    """Save (and optionally serialise) a model in order to use by `use_model`.

    The `model` can be a Path or string representing a path in which case the
    local file/folder is read and saved using the current LargeFile implementation.
    In case `model` is an object, it is serialised using `dill` before uploading it.

    Examples:
            >>> from great_ai import use_model
            >>> save_model(3, 'my_number')
            'my_number:...'

            >>> @use_model('my_number')
            ... def my_function(a, model):
            ...     return a + model
            >>> my_function(4)
            7

    Args:
        model: The object or path to be uploaded.
        key: The model's name.
        keep_last_n: If specified, remove old models and only keep the latest n. Directly passed to LargeFile.
    Returns:
        The key and version of the saved model separated by a colon. Example: "key:version"
    """
    file = get_context().large_file_implementation(
        name=key, mode="wb", keep_last_n=keep_last_n
    )

    if isinstance(model, Path) or isinstance(model, str):
        file.push(model)
    else:
        with file as f:
            dump(model, f)

    get_context().logger.info(f"Model {key} uploaded with version {file.version}")

    return f"{key}:{file.version}"
