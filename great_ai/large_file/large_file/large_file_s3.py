from hashlib import sha256
from pathlib import Path
from typing import Any, Dict, List, Optional

import boto3
from boto3.exceptions import S3UploadFailedError
from boto3.s3.transfer import TransferConfig
from botocore.exceptions import ClientError

from ...utilities import get_logger
from ..helper import DownloadProgressBar, UploadProgressBar, cached_property
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
    _configuration_attributes = (
        "region_name",
        "access_key_id",
        "secret_access_key",
        "bucket_name",
        "endpoint_url",
    )

    def _get_cache_namespace(self) -> str:
        identity = ("s3", self.endpoint_url, self.region_name, self.bucket_name)
        return sha256(repr(identity).encode()).hexdigest()

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
                "Please configure the S3 access options by calling LargeFileS3.configure_credentials or set cache_only_mode=True in the constructor."
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

        prefix = f"{self._name}{S3_NAME_VERSION_SEPARATOR}"
        parameters: Dict[str, Any] = {"Bucket": self.bucket_name, "Prefix": prefix}
        instances = []
        while True:
            page = self._client.list_objects_v2(**parameters)
            for item in page.get("Contents", []):
                key = item["Key"]
                suffix = key[len(prefix) :] if key.startswith(prefix) else ""
                if suffix.isdigit():
                    instances.append(
                        DataInstance(
                            name=self._name,
                            version=int(suffix),
                            remote_path=key,
                            cache_identity=(
                                repr((item["ETag"], item.get("LastModified")))
                                if item.get("ETag") is not None
                                else None
                            ),
                        )
                    )
            if not page.get("IsTruncated"):
                return instances
            parameters["ContinuationToken"] = page["NextContinuationToken"]

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
            Callback=(
                None
                if hide_progress
                else DownloadProgressBar(
                    name=str(remote_path), size=size, logger=logger
                )
            ),
        )

    def _upload(self, local_path: Path, hide_progress: bool) -> None:
        key = f"{self._name}/{self.version}"
        logger.info(f"Uploading {self._local_name} to S3 as {key}")

        def prevent_overwrite(params: Dict[str, Any], **_: Any) -> None:
            if params.get("Bucket") == self.bucket_name and params.get("Key") == key:
                params["IfNoneMatch"] = "*"

        # S3Transfer does not accept IfNoneMatch in ExtraArgs. These botocore
        # hooks protect both single-part and multipart commits while retaining
        # the managed transfer's streaming, retries, and progress reporting.
        events = self._client.meta.events
        operations = ("PutObject", "CompleteMultipartUpload")
        for operation in operations:
            events.register(f"before-parameter-build.s3.{operation}", prevent_overwrite)
        try:
            self._client.upload_file(
                Filename=str(local_path),
                Bucket=self.bucket_name,
                Key=key,
                Callback=(
                    None
                    if hide_progress
                    else UploadProgressBar(path=local_path, logger=logger)
                ),
                Config=TransferConfig(preferred_transfer_client="classic"),
            )
        except (ClientError, S3UploadFailedError) as error:
            cause: Optional[BaseException] = error
            while cause is not None:
                if isinstance(cause, ClientError) and cause.response["Error"][
                    "Code"
                ] in {"PreconditionFailed", "ConditionalRequestConflict", "412", "409"}:
                    raise FileExistsError(
                        f"Version {key} was created by another writer; retry the upload"
                    ) from error
                cause = cause.__cause__ or cause.__context__
            raise
        finally:
            for operation in operations:
                events.unregister(
                    f"before-parameter-build.s3.{operation}", prevent_overwrite
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
