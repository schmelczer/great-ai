import os
import threading
from logging import Logger
from typing import IO, Any, Optional

from tqdm.auto import tqdm
from pathlib import Path

import os
import sys
import threading


class ProgressBar:
    def __init__(self, file_size: int, logger: Logger, prefix: str):
        self._file_size = file_size
        self._logger = logger
        self._prefix=prefix

        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount: int):
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / float(self._file_size)) * 100
            size_length = len(str(self._file_size))
            progress = str(self._seen_so_far).rjust(size_length)
            self._logger.info(f"{self._prefix} {progress}/{self._file_size} bytes ({percentage:.1f}%)")


class DownloadProgressBar(ProgressBar):
    def __init__(self, name: str, size: int, logger: Logger):
        super().__init__(file_size=size, logger=logger, prefix=f'Downloading {name}')


class UploadProgressBar(ProgressBar):
    def __init__(self, path: Path, logger: Logger):
        size = os.path.getsize(path)
        super().__init__(file_size=size, logger=logger, prefix=f'Uploading {path.name}')
