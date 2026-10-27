import io
import tarfile
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from great_ai.large_file import LargeFileS3


def test_download_quota_keeps_the_requested_file_and_evicts_older_models(
    tmp_path: Path,
) -> None:
    backend = MagicMock()
    backend.list_objects_v2.side_effect = lambda **kwargs: {
        "Contents": [{"Key": kwargs["Prefix"] + "0", "ETag": "one"}]
    }

    def download(
        self: LargeFileS3, remote_path: Any, path: Path, hide_progress: bool
    ) -> None:
        data = b"x" * (2000 if self._name == "oversized" else 600)
        with tarfile.open(path, "w:gz") as archive:
            member = tarfile.TarInfo(self._local_name)
            member.size = len(data)
            archive.addfile(member, io.BytesIO(data))

    with (
        patch.object(LargeFileS3, "_client", backend),
        patch.object(LargeFileS3, "_download", download),
        patch.object(LargeFileS3, "cache_path", tmp_path / "cache"),
        patch.object(LargeFileS3, "max_cache_size", "1 KB"),
    ):
        first = LargeFileS3("first").get()
        second = LargeFileS3("second").get()
        assert not first.exists()
        assert second.read_bytes() == b"x" * 600
        with pytest.raises(ValueError, match="exceeds max_cache_size"):
            LargeFileS3("oversized").get()
        assert second.exists()
