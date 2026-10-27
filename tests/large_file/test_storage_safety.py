from pathlib import Path
from typing import Iterator

import pytest
from great_ai.large_file import LargeFileBase, LargeFileLocal


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
