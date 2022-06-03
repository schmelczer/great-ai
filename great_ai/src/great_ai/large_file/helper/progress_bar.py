import os
import threading
from logging import Logger
from pathlib import Path

from .bytes_to_megabytes import bytes_to_megabytes


class ProgressBar:
    min_progress_percentage_change = 10

    def __init__(self, file_size: int, logger: Logger, prefix: str):
        self._file_size = file_size
        self._logger = logger
        self._prefix = prefix

        self._last_percentage: float = 0
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount: int) -> None:
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / float(self._file_size)) * 100

            if (
                percentage != 100
                and percentage - self._last_percentage
                < self.min_progress_percentage_change
            ):
                return

            self._last_percentage += self.min_progress_percentage_change

            file_size_mb = bytes_to_megabytes(self._file_size)
            seen_so_far_mb = bytes_to_megabytes(self._seen_so_far)
            progress = seen_so_far_mb.rjust(len(file_size_mb))
            self._logger.info(
                f"{self._prefix} {progress}/{file_size_mb} MB ({percentage:.1f}%)"
            )


class DownloadProgressBar(ProgressBar):
    def __init__(self, name: str, size: int, logger: Logger):
        super().__init__(file_size=size, logger=logger, prefix=f"Downloading {name}")


class UploadProgressBar(ProgressBar):
    def __init__(self, path: Path, logger: Logger):
        size = os.path.getsize(path)
        super().__init__(file_size=size, logger=logger, prefix=f"Uploading {path.name}")
