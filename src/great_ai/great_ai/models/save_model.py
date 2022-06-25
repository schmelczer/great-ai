from pathlib import Path
from typing import Optional, Union

from joblib import dump

from ..context import get_context


def save_model(
    model: Union[Path, str, object], key: str, *, keep_last_n: Optional[int] = None
) -> str:
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
