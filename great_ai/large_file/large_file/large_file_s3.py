from functools import cached_property
from pathlib import Path
from typing import Any, List, Optional

import boto3

from ...utilities import get_logger
from ..helper import DownloadProgressBar, UploadProgressBar
from ..models import DataInstance
from .large_file_base import LargeFileBase

logger = get_logger("large_file")


S3_NAME_VERSION_SEPARATOR = "/"


class LargeFileS3(LargeFileBase):
    """LargeFile implementation using S3-compatible storage as a backend.

    Store large files remotely using the familiar API of `open()`. With built-in
    versioning, pruning and local cache.

    See parent for more details.
    """

    region_name = None
    access_key_id = None
    secret_access_key = None
    bucket_name = None
    endpoint_url = None

    @classmethod
    def configure_credentials(  # type: ignore
        cls,
        *,
        aws_region_name: str,
        aws_access_key_id: str,
        aws_secret_access_key: str,
        large_files_bucket_name: str,
        aws_endpoint_url: Optional[str] = None,
        **_: Any,
    ) -> None:
        cls.region_name = aws_region_name
        cls.access_key_id = aws_access_key_id
        cls.secret_access_key = aws_secret_access_key
        cls.bucket_name = large_files_bucket_name
        cls.endpoint_url = aws_endpoint_url
        super().configure_credentials()

    @cached_property
    def _client(self) -> boto3.client:
        if (
            self.region_name is None
            or self.access_key_id is None
            or self.secret_access_key is None
            or self.bucket_name is None
        ):
            raise ValueError(
                "Please configure the S3 access options by calling LargeFileS3.configure_credentials or set offline_mode=True in the constructor."
            )

        return boto3.client(
            "s3",
            aws_access_key_id=self.access_key_id,
            aws_secret_access_key=self.secret_access_key,
            region_name=self.region_name,
            endpoint_url=self.endpoint_url,
        )

    def _find_remote_instances(self) -> List[DataInstance]:
        logger.debug(f"Fetching S3 versions of {self._name}")

        found_objects = self._client.list_objects_v2(
            Bucket=self.bucket_name, Prefix=self._name
        )
        return (
            [
                DataInstance(
                    name=o["Key"].split(S3_NAME_VERSION_SEPARATOR)[0],
                    version=int(o["Key"].split(S3_NAME_VERSION_SEPARATOR)[-1]),
                    remote_path=o["Key"],
                )
                for o in found_objects["Contents"]
                if o["Key"].split(S3_NAME_VERSION_SEPARATOR)[0] == self._name
            ]
            if "Contents" in found_objects
            else []
        )

    def _download(
        self, remote_path: Any, local_path: Path, hide_progress: bool
    ) -> None:
        logger.info(f"Downloading {remote_path} from S3")

        size = self._client.head_object(Bucket=self.bucket_name, Key=remote_path)[
            "ContentLength"
        ]

        self._client.download_file(
            Bucket=self.bucket_name,
            Key=remote_path,
            Filename=str(local_path),
            Callback=None
            if hide_progress
            else DownloadProgressBar(name=str(remote_path), size=size, logger=logger),
        )

    def _upload(self, local_path: Path, hide_progress: bool) -> None:
        key = f"{self._name}/{self.version}"
        logger.info(f"Uploading {self._local_name} to S3 as {key}")

        self._client.upload_file(
            Filename=str(local_path),
            Bucket=self.bucket_name,
            Key=key,
            Callback=None
            if hide_progress
            else UploadProgressBar(path=local_path, logger=logger),
        )

    def _delete_old_remote_versions(self) -> None:
        if self._keep_last_n is not None:
            for i in (
                self._instances[: -self._keep_last_n]
                if self._keep_last_n > 0
                else self._instances
            ):
                logger.info(
                    f"Removing old version from S3 (keep_last_n={self._keep_last_n}): {i.remote_path}"
                )
                self._client.delete_object(Bucket=self.bucket_name, Key=i.remote_path)
