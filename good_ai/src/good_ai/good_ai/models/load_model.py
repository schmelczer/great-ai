import logging
from typing import Any, Optional, Tuple

from joblib import load

from good_ai.open_s3 import LargeFile

from ..context import get_context

logger = logging.getLogger("models")


def load_model(
    key: str, version: Optional[int] = None, return_path: bool = False
) -> Tuple[Any, int]:
    get_context()  # will setup LargeFile if there was no config set

    file = LargeFile(name=key, mode="rb", version=version)

    if return_path:
        return file.get(), file.version

    with file as f:
        return load(f), file.version
