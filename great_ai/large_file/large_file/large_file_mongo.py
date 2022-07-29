import re
from pathlib import Path
from typing import Any, List

from gridfs import DEFAULT_CHUNK_SIZE, Database, GridFSBucket
from pymongo import MongoClient

from ...utilities import get_logger
from ..helper import DownloadProgressBar, UploadProgressBar, cached_property
from ..models import DataInstance
from .large_file_base import LargeFileBase

logger = get_logger("large_file")


MONGO_NAME_VERSION_SEPARATOR = "_"


class LargeFileMongo(LargeFileBase):
    """LargeFile implementation using GridFS (MongoDB) as a backend.

    Store large files remotely using the familiar API of `open()`. With built-in
    versioning, pruning and local cache.

    See parent for more details.
    """

    mongo_connection_string = None
    mongo_database = None

    @classmethod
    def configure_credentials(  # type: ignore
        cls,
        *,
        mongo_connection_string: str,
        mongo_database: str,
        **_: Any,
    ) -> None:
        cls.mongo_connection_string = mongo_connection_string
        cls.mongo_database = mongo_database
        super().configure_credentials()

    @cached_property
    def _client(self) -> GridFSBucket:
        if self.mongo_connection_string is None or self.mongo_database is None:
            raise ValueError(
                "Please configure the MongoDB access options by calling LargeFileMongo.configure_credentials or set offline_mode=True in the constructor."
            )

        db: Database = MongoClient(self.mongo_connection_string)[self.mongo_database]
        return GridFSBucket(db)

    def _find_remote_instances(self) -> List[DataInstance]:
        logger.debug(f"Fetching Mongo (GridFS) versions of {self._name}")

        return [
            DataInstance(
                name=MONGO_NAME_VERSION_SEPARATOR.join(
                    f.name.split(MONGO_NAME_VERSION_SEPARATOR)[:-1]
                ),
                version=int(f.name.split(MONGO_NAME_VERSION_SEPARATOR)[-1]),
                remote_path=(f._id, f.length),
                origin="mongodb",
            )
            for f in self._client.find(
                {
                    "filename": re.compile(
                        re.escape(self._name + MONGO_NAME_VERSION_SEPARATOR) + ".*"
                    )
                }
            )
        ]

    def _download(
        self, remote_path: Any, local_path: Path, hide_progress: bool
    ) -> None:
        logger.info(f"Downloading {remote_path[0]} from Mongo (GridFS)")

        progress = (
            DownloadProgressBar(
                name=str(remote_path[0]), size=remote_path[1], logger=logger
            )
            if not hide_progress
            else None
        )
        with self._client.open_download_stream(remote_path[0]) as stream:
            with open(local_path, "wb") as f:
                while True:
                    content = stream.read(DEFAULT_CHUNK_SIZE)
                    f.write(content)

                    if progress:
                        progress(len(content))
                    if len(content) < DEFAULT_CHUNK_SIZE:
                        break

    def _upload(self, local_path: Path, hide_progress: bool) -> None:
        logger.info(f"Uploading {local_path} to Mongo (GridFS)")

        progress = (
            UploadProgressBar(path=local_path, logger=logger)
            if not hide_progress
            else None
        )
        with self._client.open_upload_stream(
            f"{self._name}{MONGO_NAME_VERSION_SEPARATOR}{self.version}"
        ) as stream:
            with open(local_path, "rb") as f:
                while True:
                    content = f.read(DEFAULT_CHUNK_SIZE)
                    stream.write(content)

                    if progress:
                        progress(len(content))
                    if len(content) < DEFAULT_CHUNK_SIZE:
                        break

    def _delete_old_remote_versions(self) -> None:
        if self._keep_last_n is not None:
            for i in (
                self._instances[: -self._keep_last_n]
                if self._keep_last_n > 0
                else self._instances
            ):
                logger.info(
                    f"Removing old version from MongoDB (GridFS) (keep_last_n={self._keep_last_n}): {i.name}{MONGO_NAME_VERSION_SEPARATOR}{i.version}"
                )
                self._client.delete(i.remote_path[0])
