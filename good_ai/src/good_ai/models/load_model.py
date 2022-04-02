import logging
from typing import Any, Optional

from joblib import load
from open_s3 import LargeFile

logger = logging.getLogger("models")


def load_model(
    key: str, version: Optional[int] = None, return_path: bool = False
) -> Any:
    file = LargeFile(name=key, mode="rb", version=version)

    if return_path:
        return file.get()

    with file as f:
        return load(f)
