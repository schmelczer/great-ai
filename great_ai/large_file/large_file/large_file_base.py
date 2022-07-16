import os
import shutil
import tempfile
from abc import ABC, abstractmethod
from functools import lru_cache
from pathlib import Path
from types import TracebackType
from typing import IO, Any, List, Literal, Optional, Type, Union, cast

from great_ai.utilities import ConfigFile, get_logger

from ..helper import human_readable_to_byte
from ..models import DataInstance

logger = get_logger("large_file")


CACHE_NAME_VERSION_SEPARATOR = "-"
COMPRESSION_ALGORITHM = "gztar"
ARCHIVE_EXTENSION = ".tar.gz"


class LargeFileBase(ABC):
    """Base for LargeFile implementations with different backends.

    Store large files remotely using the familiar API of `open()`. With built-in
    versioning, pruning and local cache.

    By default, files are stored in the ".cache" folder and the least recently used is
    deleted after the overall size reaches 30 GBs.

    Examples:
        >>> LargeFileBase.cache_path = Path(".cache")

        >>> LargeFileBase.max_cache_size = "30GB"

    Attributes:
        initialized: Tell whether `configure_credentials` or
            `configure_credentials_from_file` has been already called.
        cache_path: Storage location for cached files.
        max_cache_size: Delete files until the folder at `cache_path` is smaller than
            this value. Examples: "5 GB", "10MB", "0.3 TB". Set to `None` for no
            automatic cache-pruning.
    """

    initialized = False
    cache_path = Path(".cache")
    max_cache_size: Optional[str] = "30GB"

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
        cache_only_mode: bool = False,
    ):
        self._name = name
        self._version = version
        self._mode = mode
        self._keep_last_n = keep_last_n
        self._cache_only_mode = cache_only_mode

        self._buffering = buffering
        self._encoding = encoding
        self._errors = errors
        self._newline = newline

        LargeFileBase.cache_path.mkdir(parents=True, exist_ok=True)

        self._find_instances()
        self._check_mode_and_set_version()

    @classmethod
    def configure_credentials_from_file(
        cls,
        secrets: Union[Path, str, ConfigFile],
    ) -> None:
        """Load file and feed its content to `configure_credentials`.

        Extra keys are ignored.
        """

        if not isinstance(secrets, ConfigFile):
            secrets = ConfigFile(secrets)
        cls.configure_credentials(**{k.lower(): v for k, v in secrets.items()})

    @classmethod
    def configure_credentials(cls, **kwargs: str) -> None:
        """Configure required credentials for the LargeFile backend."""

        cls.initialized = True

    def __enter__(self) -> IO:
        self._file: IO[Any] = (
            tempfile.NamedTemporaryFile(
                mode=self._mode,
                buffering=self._buffering,
                encoding=self._encoding,
                newline=self._newline,
                errors=self._errors,
                delete=False,
                prefix="large_file-",
            )
            if "w" in self._mode
            else open(
                self.get(),
                mode=self._mode,
                buffering=self._buffering,
                encoding=self._encoding,
                newline=self._newline,
                errors=self._errors,
            )
        )

        return self._file

    def __exit__(
        self,
        type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Literal[False]:
        self._file.close()

        if type is None:
            if "w" in self._mode:
                self.push(Path(self._file.name))
                os.unlink(self._file.name)
        else:
            logger.exception("Could not finish operation.")

        return False

    @property
    def version(self) -> int:
        """Numeric version of the file proxied by this LargeFile instance."""

        return cast(int, self._version)

    @lru_cache(1)
    def get(self, hide_progress: bool = False) -> Path:
        """Return path to the proxy of a file (or directory).

        If not available in the local cache, an attempt is made to download it.

        Args:
            hide_progress: Do not show a progress update after each 10% of progress.
        """

        remote_path = next(
            i.remote_path for i in self._instances if i.version == self._version
        )

        destination = self.cache_path / self._local_name
        if not destination.exists():
            logger.info(f"File {self._local_name} does not exist locally")

            with tempfile.TemporaryDirectory() as tmp:
                local_root_path = Path(tmp)
                tmp_file_archive = (
                    local_root_path / f"{self._local_name}{ARCHIVE_EXTENSION}"
                )
                self._download(
                    remote_path, tmp_file_archive, hide_progress=hide_progress
                )

                logger.info(f"Decompressing {self._local_name}")
                shutil.unpack_archive(str(tmp_file_archive), tmp, COMPRESSION_ALGORITHM)
                shutil.move(str(local_root_path / self._local_name), str(destination))
        else:
            logger.info(f"File {self._local_name} found in cache")

        return destination

    def push(self, path: Union[Path, str], hide_progress: bool = False) -> None:
        """Upload a file (or directory) as a new version of `key`.

        The file/directory is compressed before upload.

        Args:
            hide_progress: Do not show a progress update after each 10% of progress.
        """

        if isinstance(path, str):
            path = Path(path)

        with tempfile.TemporaryDirectory() as tmp:
            if path.is_file():
                logger.info(f"Copying file for {self._local_name}")
                copy: Any = shutil.copy
            else:
                logger.info(f"Copying directory for {self._local_name}")
                copy = shutil.copytree

            try:
                # Make local copy in the cache
                shutil.rmtree(self.cache_path / self._local_name, ignore_errors=True)
                copy(str(path), str(self.cache_path / self._local_name))
            except shutil.SameFileError:
                pass  # No worries

            copy(str(path), str(Path(tmp) / self._local_name))

            with tempfile.TemporaryDirectory() as tmp2:
                # A directory has to be zipped and it cannot contain the output of the zipping
                logger.info(f"Compressing {self._local_name}")
                shutil.make_archive(
                    str(Path(tmp2) / self._local_name),
                    COMPRESSION_ALGORITHM,
                    tmp,
                )

                file_to_be_uploaded = (
                    Path(tmp2) / f"{self._local_name}{ARCHIVE_EXTENSION}"
                )
                self._upload(file_to_be_uploaded, hide_progress=hide_progress)

        self.clean_up()

    def delete(self) -> None:
        """Delete all versions of the files under this `key`."""

        self._keep_last_n = 0
        self._delete_old_remote_versions()

    @property
    def versions_pretty(self) -> str:
        """Formatted string of all available versions."""
        return ", ".join((str(i.version) for i in self._instances))

    def clean_up(self) -> None:
        """Delete local and remote versions according to currently set cache and retention policy."""

        self._delete_old_remote_versions()
        self._prune_cache()

    @property
    def _local_name(self) -> str:
        return f"{self._name}{CACHE_NAME_VERSION_SEPARATOR}{self.version}"

    def _find_instances(self) -> None:
        if self._cache_only_mode:
            self._instances = self._find_instances_from_cache()
        else:
            self._instances = self._find_remote_instances()

        self._instances = sorted(self._instances, key=lambda i: i.version)

    def _find_instances_from_cache(self) -> List[DataInstance]:
        logger.info(f"Fetching cached versions of {self._name}")

        candidates = [
            DataInstance(
                name=CACHE_NAME_VERSION_SEPARATOR.join(
                    f.name.split(CACHE_NAME_VERSION_SEPARATOR)[:-1]
                ),
                version=int(f.name.split(CACHE_NAME_VERSION_SEPARATOR)[-1]),
                remote_path=f,
            )
            for f in self.cache_path.glob(
                f"{self._name}{CACHE_NAME_VERSION_SEPARATOR}*"
            )
        ]

        return [c for c in candidates if c.name == self._name]

    def _check_mode_and_set_version(self) -> None:
        if "+" in self._mode:
            raise ValueError(
                f"File mode `{self._mode}` is not allowed3, remove the `+`."
            )

        if "w" in self._mode:
            if self._version is not None:
                raise ValueError("Providing a version is not allowed in write mode.")

            self._version = self._instances[-1].version + 1 if self._instances else 0

        elif "r" in self._mode:
            if not self._instances:
                raise FileNotFoundError(
                    f"File {self._name} not found. No versions are available."
                )

            if self._version is None:
                self._version = self._instances[-1].version
                logger.info(
                    f"Latest version of {self._name} is {self._version} "
                    + f"(from versions: {self.versions_pretty})"
                )
            elif self._version not in [i.version for i in self._instances]:
                raise FileNotFoundError(
                    f"File {self._name} not found with version {self._version}. "
                    + f"(from versions: {self.versions_pretty})"
                )
        else:
            raise ValueError("Unsupported file mode.")

    def _prune_cache(self) -> None:
        self.cache_path.mkdir(parents=True, exist_ok=True)

        if self.max_cache_size is None:
            return

        allowed_size = human_readable_to_byte(self.max_cache_size)
        assert allowed_size >= 0

        least_recently_read = sorted(
            [f for f in self.cache_path.glob("*")], key=lambda f: f.stat().st_atime
        )

        while sum(os.path.getsize(f) for f in least_recently_read) > allowed_size:
            file = least_recently_read.pop(0)
            logger.info(
                f"Deleting file from cache to meet quota (max_cache_size={self.max_cache_size}): {file}"
            )
            os.unlink(file)

    @abstractmethod
    def _find_remote_instances(self) -> List[DataInstance]:
        pass

    @abstractmethod
    def _download(
        self, remote_path: Any, local_path: Path, hide_progress: bool
    ) -> None:
        pass

    @abstractmethod
    def _upload(self, local_path: Path, hide_progress: bool) -> None:
        pass

    @abstractmethod
    def _delete_old_remote_versions(self) -> None:
        pass
