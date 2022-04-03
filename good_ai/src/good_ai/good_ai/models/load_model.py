import logging
from typing import Any, Optional, Tuple

from joblib import load

from good_ai.open_s3 import LargeFile

from ..set_default_config import set_default_config_if_uninitialized

logger = logging.getLogger("models")


def load_model(
    key: str, version: Optional[int] = None, return_path: bool = False
) -> Tuple[Any, int]:
    set_default_config_if_uninitialized()

    file = LargeFile(name=key, mode="rb", version=version)

    if return_path:
        return file.get(), file.version

    with file as f:
        return load(f), file.version
