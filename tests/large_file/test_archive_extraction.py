import io
import tarfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from great_ai.large_file import LargeFileS3


def test_remote_archive_cannot_escape_cache(tmp_path: Path) -> None:
    backend = MagicMock()
    backend.list_objects_v2.return_value = {"Contents": [{"Key": "model/0"}]}
    sentinel = tmp_path / "escaped"

    def download(
        self: LargeFileS3, remote_path: str, local_path: Path, hide_progress: bool
    ) -> None:
        with tarfile.open(local_path, "w:gz") as archive:
            member = tarfile.TarInfo("../escaped")
            member.size = 7
            archive.addfile(member, io.BytesIO(b"payload"))

    with (
        patch.object(LargeFileS3, "cache_path", tmp_path / "cache"),
        patch.object(LargeFileS3, "_client", backend),
        patch.object(LargeFileS3, "_download", download),
        patch("tempfile.tempdir", str(tmp_path)),
    ):
        with pytest.raises(tarfile.OutsideDestinationError):
            LargeFileS3("model").get()
    assert not sentinel.exists()
