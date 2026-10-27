from pathlib import Path
from typing import Iterator

import pytest
from great_ai import RouteConfig, configure, context
from great_ai.large_file import LargeFileBase, LargeFileLocal


@pytest.fixture
def isolated_context(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Iterator[None]:
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(context, "_context", None)
    monkeypatch.setattr(context, "DEFAULT_TRACING_DATABASE_CONFIG_PATHS", {})
    monkeypatch.setattr(context, "DEFAULT_LARGE_FILE_CONFIG_PATHS", {})
    for implementation in (LargeFileBase, LargeFileLocal):
        monkeypatch.setattr(implementation, "cache_path", tmp_path / "cache")
        monkeypatch.setattr(implementation, "max_cache_size", None)
    configure(
        disable_se4ml_banner=True,
        should_log_exception_stack=False,
        route_config=RouteConfig(dashboard_enabled=False),
    )
    yield
