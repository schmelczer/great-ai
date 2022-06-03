from typing import Any, Optional, Tuple

from joblib import load

from ..context import get_context


def load_model(
    key: str, version: Optional[int] = None, return_path: bool = False
) -> Tuple[Any, int]:
    file = get_context().large_file_implementation(name=key, mode="rb", version=version)

    if return_path:
        return file.get(), file.version

    with file as f:
        return load(f), file.version
