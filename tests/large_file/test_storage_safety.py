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
