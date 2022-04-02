import configparser
import logging
import os
import shutil
import tempfile
from pathlib import Path
from types import TracebackType
from typing import IO, Any, Dict, List, Optional, Type, Union
import boto3
from botocore.exceptions import ClientError

from helper import DownloadProgressBar, UploadProgressBar, human_readable_to_byte

logger = logging.getLogger("open_s3")


class LargeFile:
    """
    Store large files in S3. Use local cache for speed up.

    Examples:

    ```
    with LargeFile("test.txt", "w", keep_last_n=3) as f:
        for i in range(1000000):
            f.write('test\n')

    with LargeFile("test.txt", "r") as f:
        print(f.readlines()[0])

    path_to_cached_text_file = LargeFile("test.txt", version=0).get()
    ```

    By default, files are stored in the ".cache" folder and the
    least recently use is deleted after the overall size reaches 30 GBs.

    Change it with the following properties.

    ```
    LargeFile.cache_path = Path(".cache")
    LargeFile.max_cache_size = "30GB"
    ```
    """

    region_name = None
    access_key_id = None
    secret_access_key = None
    bucket_name = None
    endpoint_url = None

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
        offline_mode: bool = False
    ):
        self._name: str = name
        self._version = version
        self._mode: str = mode
        self._keep_last_n = keep_last_n
        self._offline_mode = offline_mode

        self._buffering = buffering
        self._encoding = encoding
        self._errors = errors
        self._newline = newline

        LargeFile.cache_path.mkdir(parents=True, exist_ok=True)

        self._find_versions()
        self._check_mode_and_set_version()
        
    @classmethod
    def configure_credentials(
        cls,
        *,
        aws_region_name: str,
        aws_access_key_id: str,
        aws_secret_access_key: str,
        large_files_bucket_name: str,
        endpoint_url: Optional[str] = None,
        **_: Dict[str, Any],
    ) -> None:
        cls.region_name = aws_region_name
        cls.access_key_id = aws_access_key_id
        cls.secret_access_key = aws_secret_access_key
        cls.bucket_name = large_files_bucket_name
        cls.endpoint_url = endpoint_url

    @classmethod
    def configure_credentials_from_file(
        cls,
        secrets_path: Union[Path, str],
    ) -> None:

        if isinstance(secrets_path, str):
            secrets_path = Path(secrets_path)

        if not secrets_path.exists():
            raise FileNotFoundError(secrets_path.resolve())

        credentials = configparser.ConfigParser()
        credentials.read(secrets_path)
        credentials.default_section
        cls.configure_credentials(**credentials[credentials.default_section])

    def __enter__(self) -> IO:
        self._file: IO[Any] = (
            tempfile.NamedTemporaryFile(
                mode=self._mode,
                buffering=self._buffering,
                encoding=self._encoding,
                newline=self._newline,
                errors=self._errors,
                delete=False,
                prefix="large-file-",
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
    ) -> bool:
        self._file.close()

        if type is None:
            if "w" in self._mode:
                self.push(Path(self._file.name))
                os.unlink(self._file.name)
        else:
            logger.exception("Could not finish operation.")

        return True
    
    @property
    def version_ids(self) -> List[int]:
        return [self._get_version_from_key(key) for key in self._versions]

    def get(self, hide_progress: bool = False) -> Path:
        key = next(
            key
            for key in self._versions
            if self._get_version_from_key(key) == self._version
        )

        destination = self.cache_path / self._local_name
        if not destination.exists():
            logger.info(
                f"File {self._local_name} does not exist locally, starting download from S3"
            )

            with tempfile.TemporaryDirectory() as tmp:
                tmp_file_archive = Path(tmp) / f"{self._local_name}.tar.gz"

                size = self._client.head_object(Bucket=self.bucket_name, Key=key)['ContentLength']
                self._client.download_file(Bucket=self.bucket_name, Key=key, Filename=str(tmp_file_archive), Callback=None if hide_progress else DownloadProgressBar(size=size, name=key, logger=logger))
                logger.info(f"Decompressing {self._local_name}")
                shutil.unpack_archive(str(tmp_file_archive), tmp, "gztar")
                tmp_file = Path(tmp) / self._local_name
                shutil.move(str(tmp_file), str(destination))
        else:
            logger.info(f"File {self._local_name} found in cache")

        return destination

    def push(self, path: Union[Path, str], hide_progress: bool = False) -> None:
        if isinstance(path, str):
            path = Path(path)

        with tempfile.TemporaryDirectory() as tmp:
            if path.is_file():
                logger.info(f"Copying file for {self._local_name}")
                copy = shutil.copy 
            else:
                logger.info(f"Copying directory for {self._local_name}")
                copy = shutil.copytree

            try:
                # Make local copy in the cache
                copy(str(path), str(self.cache_path / self._local_name))
            except shutil.SameFileError:
                pass  # No worries

            copy(str(path), str(Path(tmp) / self._local_name))

            logger.info(f"Compressing {self._local_name}")
            shutil.make_archive(
                str(Path(tmp) / self._local_name),
                "gztar",
                tmp,
            )

            logger.info(f"Uploading {self._local_name} to S3 from {path}")

            file_to_be_uploaded = Path(tmp) / f"{self._local_name}.tar.gz"
            self._client.upload_file(Filename=str(file_to_be_uploaded), Bucket=self.bucket_name, Key=self._s3_name, Callback=None if hide_progress else UploadProgressBar(file_to_be_uploaded, logger=logger))

        self.clean_up()

    def delete(self) -> None:
        self._keep_last_n = 0
        self._delete_old_versions_from_s3()

    def clean_up(self) -> None:
        self._delete_old_versions_from_s3()
        self._delete_old_versions_from_disk()

    def _create_client(self) -> None:
        if (
            self.region_name is None
            or self.access_key_id is None
            or self.secret_access_key is None
            or self.bucket_name is None
        ):
            raise ValueError(
                "Please configure the S3 access options by calling LargeFile.configure_credentials or set offline_mode=True in the constructor."
            )

        self._client = boto3.client('s3', aws_access_key_id=self.access_key_id, aws_secret_access_key=self.secret_access_key, region_name=self.region_name, endpoint_url=self.endpoint_url)
        
    def _find_versions(self) -> None:
        if self._offline_mode:
            self._fetch_versions_from_cache()
        else:
            self._create_client()
            self._fetch_versions_from_s3()
        
        if self._versions:
            logger.info(f"Found versions: {self.version_ids}")
        else:
            logger.info("No versions found")

    def _fetch_versions_from_cache(self) -> None:
        logger.info(f"Fetching offline versions of {self._name}")

        self._versions = [
            path
            for path in self.cache_path.glob(f'{self._local_name}-*')
        ]

    def _fetch_versions_from_s3(self) -> None:
        logger.info(f"Fetching online versions of {self._name}")
        found_objects = self._client.list_objects_v2(
            Bucket=self.bucket_name, Prefix=self._name
        )
        self._versions = (
            sorted(
                o["Key"]
                for o in found_objects["Contents"]
            )
            if "Contents" in found_objects
            else []
        )

    def _check_mode_and_set_version(self) -> None:
        if "+" in self._mode:
            raise ValueError("Read-write mode is not allowed.")

        if "w" in self._mode:
            if self._version is not None:
                raise ValueError("Providing a version is not allowed in write mode.")

            self._version = self.version_ids[-1] + 1 if self.version_ids else 0

        elif "r" in self._mode:
            if not self.version_ids:
                raise FileNotFoundError(
                    f"File {self._name} not found. No versions are available."
                )

            if self._version is None:
                self._version = self.version_ids[-1]
                logger.info(f"Lastest version of {self._local_name} is {self._version}")

            elif self._version not in self.version_ids:
                raise FileNotFoundError(
                    f"File {self._name} not found with version {self._version}. Available versions: {self.version_ids}"
                )
        else:
            raise ValueError("Unsupported file mode.")

    @property
    def _local_name(self) -> str:
        return f"{self._name}-{self._version}"

    @property
    def _s3_name(self) -> str:
        return f"{self._name}/{self._version}"
        
    @staticmethod
    def _get_version_from_key(key: Union[str, Path]) -> int:
        if isinstance(key, Path):
            return int(key.name.split("-")[-1])
        return int(key.split("/")[-1])


    def _delete_old_versions_from_s3(self) -> None:
        if self._keep_last_n is not None:
            for key in (self._versions[: -self._keep_last_n] if self._keep_last_n > 0 else self._versions):
                logger.info(
                    f"Removing old version (keep_last_n={self._keep_last_n}): {key}"
                )
                self._client.delete_object(Bucket=self.bucket_name, Key=key)
                
    def _delete_old_versions_from_disk(self) -> None:
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