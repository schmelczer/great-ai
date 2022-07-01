from typing import Any, Optional, Tuple

from joblib import load

from ..context import get_context


def load_model(key: str, version: Optional[int] = None) -> Tuple[Any, int]:
    file = get_context().large_file_implementation(name=key, mode="rb", version=version)

    path = file.get()

    if path.is_dir():
        return path, file.version

    with file as f:
        return load(f), file.version
