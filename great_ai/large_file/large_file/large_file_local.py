from pathlib import Path
from typing import Any, List, Optional

from ...utilities import get_logger
from ..models import DataInstance
from .large_file_base import LargeFileBase

logger = get_logger("large_file")


class LargeFileLocal(LargeFileBase):
    """LargeFile implementation using local filesystem as a backend.

    Store large files remotely using the familiar API of `open()`. With built-in
    versioning, pruning and local cache.

    IMPORTANT: If LargeFileLocal.max_cache_size is too small, it won't be enough to
    store all your files and they can end up deleted.

    See parent for more details.

    Examples:
        >>> LargeFileLocal.cache_path = Path(".cache")

        >>> LargeFileLocal.max_cache_size = "30GB"

        >>> with LargeFileLocal("my_test.txt", "w", keep_last_n=2) as f:
        ...     f.write('test')
        4

        >>> with LargeFileLocal("my_test.txt") as f:
        ...     print(f.read())
        test
    """

    def __init__(
        self,
        name: str,
        mode: str = "r",
        *,
        buffering: int = -1,
        encoding: Optional[str] = None,
        errors: Optional[str] = None,
        newline: Optional[str] = None,
        version: Optional[int] = None,
        keep_last_n: Optional[int] = None,
    ):
        super().__init__(
            name,
            mode,
            buffering=buffering,
            encoding=encoding,
            errors=errors,
            newline=newline,
            version=version,
            keep_last_n=keep_last_n,
            cache_only_mode=True,
        )
        super().configure_credentials()

    def _find_remote_instances(self) -> List[DataInstance]:
        return []

    def _download(
        self, remote_path: Any, local_path: Path, hide_progress: bool
    ) -> None:
        # This will never be called because the file must be in the cache
        raise NotImplementedError()

    def _upload(self, local_path: Path, hide_progress: bool) -> None:
        pass  # the "upload" is already done py the parent's caching mechanism

    def _delete_old_remote_versions(self) -> None:
        if self._keep_last_n is not None:
            for i in (
                self._instances[: -self._keep_last_n]
                if self._keep_last_n > 0
                else self._instances
            ):
                logger.info(
                    f"Removing old version (keep_last_n={self._keep_last_n}): {i.remote_path}"
                )
                i.remote_path.unlink()
