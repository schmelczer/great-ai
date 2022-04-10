from pathlib import Path
from typing import Optional, Union

from joblib import dump

from good_ai.open_s3 import LargeFile

from ..context import get_context


def save_model(
    model: Union[Path, str, object], key: str, keep_last_n: Optional[int] = None
) -> int:
    get_context()  # will setup LargeFile if there was no config set

    file = LargeFile(name=key, mode="wb", keep_last_n=keep_last_n)

    if isinstance(model, Path) or isinstance(model, str):
        file.push(model)
    else:
        with file as f:
            dump(model, f)

    get_context().logger.info(f"Model {key} uploaded with version {file.version}")

    return file.version
