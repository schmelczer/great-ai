import io
import tarfile
import time
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
from pathlib import Path
from typing import Any, Dict
from unittest.mock import MagicMock, patch

from great_ai.large_file import LargeFileS3


def test_recreated_remote_version_invalidates_other_clients(tmp_path: Path) -> None:
    remote: Dict[str, bytes] = {}
    backend = MagicMock()
    backend.list_objects_v2.side_effect = lambda **kwargs: {
        "Contents": [
            {"Key": key, "ETag": sha256(value).hexdigest()}
            for key, value in remote.items()
        ]
    }
    backend.delete_object.side_effect = lambda **kwargs: remote.pop(kwargs["Key"])

    def upload(self: LargeFileS3, path: Path, hide_progress: bool) -> None:
        remote[f"{self._name}/{self.version}"] = path.read_bytes()

    def download(
        self: LargeFileS3, remote_path: Any, path: Path, hide_progress: bool
    ) -> None:
        path.write_bytes(remote[remote_path])

    with (
        patch.object(LargeFileS3, "_client", backend),
        patch.object(LargeFileS3, "_upload", upload),
        patch.object(LargeFileS3, "_download", download),
        patch.object(LargeFileS3, "max_cache_size", None),
    ):
        with patch.object(LargeFileS3, "cache_path", tmp_path / "writer"):
            with LargeFileS3("model", "w") as file:
                file.write("old")
        with patch.object(LargeFileS3, "cache_path", tmp_path / "reader"):
            reader = LargeFileS3("model")
            assert reader.get().read_text() == "old"
        with patch.object(LargeFileS3, "cache_path", tmp_path / "writer"):
            LargeFileS3("model").delete()
            with LargeFileS3("model", "w") as file:
                file.write("new")
            assert LargeFileS3("model").get().read_text() == "new"
        with patch.object(LargeFileS3, "cache_path", tmp_path / "reader"):
            assert reader.get().read_text() == "new"


def test_concurrent_downloads_publish_one_directory(tmp_path: Path) -> None:
    backend = MagicMock()
    backend.list_objects_v2.return_value = {
        "Contents": [{"Key": "model/0", "ETag": "one"}]
    }
    downloads = []

    def download(
        self: LargeFileS3, remote_path: Any, path: Path, hide_progress: bool
    ) -> None:
        downloads.append(remote_path)
        time.sleep(0.1)
        with tarfile.open(path, "w:gz") as archive:
            folder = tarfile.TarInfo("model-0")
            folder.type = tarfile.DIRTYPE
            folder.mode = 0o755
            archive.addfile(folder)
            file = tarfile.TarInfo("model-0/weights")
            file.size = 7
            file.mode = 0o644
            archive.addfile(file, io.BytesIO(b"weights"))

    with (
        patch.object(LargeFileS3, "_client", backend),
        patch.object(LargeFileS3, "_download", download),
        patch.object(LargeFileS3, "cache_path", tmp_path / "cache"),
        ThreadPoolExecutor(max_workers=2) as pool,
    ):
        readers = [LargeFileS3("model") for _ in range(2)]
        results = list(pool.map(lambda reader: reader.get(), readers))
    assert results[0] == results[1]
    assert list(results[0].iterdir()) == [results[0] / "weights"]
    assert (results[0] / "weights").read_text() == "weights"
    assert downloads == ["model/0"]
