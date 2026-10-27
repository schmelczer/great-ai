import io
import tarfile
from pathlib import Path
from typing import Any, Iterator
from unittest.mock import MagicMock, patch

import pytest
from great_ai.large_file import LargeFileBase, LargeFileLocal, LargeFileS3


@pytest.fixture(autouse=True)
def storage(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Iterator[None]:
    for implementation in (LargeFileBase, LargeFileLocal):
        monkeypatch.setattr(implementation, "cache_path", tmp_path / "cache")
        monkeypatch.setattr(implementation, "max_cache_size", None)
    yield


def test_configured_cache_directory_is_created(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(LargeFileLocal, "cache_path", tmp_path / "custom-cache")
    with LargeFileLocal("model", "w") as file:
        file.write("weights")
    assert LargeFileLocal("model").get().read_text() == "weights"


def test_unrelated_cache_entries_are_ignored() -> None:
    LargeFileLocal.cache_path.mkdir(parents=True)
    (LargeFileLocal.cache_path / "model-unrelated").write_text("unrelated")
    (LargeFileLocal.cache_path / "model-0").write_text("weights")
    assert LargeFileLocal("model").get().read_text() == "weights"


@pytest.mark.parametrize("operation", ["delete", "prune"])
def test_cached_directories_can_be_removed(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, operation: str
) -> None:
    source = tmp_path / "source"
    source.mkdir()
    (source / "weights").write_text("weights")
    LargeFileLocal("model", "w").push(source)
    reader = LargeFileLocal("model")
    cached = reader.get()
    if operation == "delete":
        reader.delete()
    else:
        monkeypatch.setattr(LargeFileLocal, "max_cache_size", "0")
        reader.clean_up()
    assert not cached.exists()


def test_cache_quota_counts_directory_contents(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source = tmp_path / "source"
    source.mkdir()
    (source / "weights").write_bytes(b"x" * 100_000)
    monkeypatch.setattr(LargeFileLocal, "max_cache_size", "1 KB")
    LargeFileLocal("model", "w").push(source)
    assert not (LargeFileLocal.cache_path / "model-0").exists()


def test_failed_write_removes_temporary_file() -> None:
    temporary = None
    try:
        with pytest.raises(ValueError, match="failed"):
            with LargeFileLocal("model", "w") as file:
                temporary = Path(file.name)
                file.write("unfinished")
                raise ValueError("failed")
        assert temporary is not None
        assert not temporary.exists()
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def test_evicted_remote_model_is_downloaded_again() -> None:
    backend = MagicMock()
    backend.list_objects_v2.return_value = {"Contents": [{"Key": "model/0"}]}
    downloads = []

    def download(
        self: LargeFileS3, remote_path: Any, local_path: Path, hide_progress: bool
    ) -> None:
        downloads.append(remote_path)
        with tarfile.open(local_path, "w:gz") as archive:
            payload = b"remote weights"
            member = tarfile.TarInfo("model-0")
            member.size = len(payload)
            archive.addfile(member, io.BytesIO(payload))

    with (
        patch.object(LargeFileS3, "_client", backend),
        patch.object(LargeFileS3, "_download", download),
    ):
        reader = LargeFileS3("model")
        cached = reader.get()
        cached.unlink()
        assert reader.get().read_text() == "remote weights"
    assert downloads == ["model/0", "model/0"]
