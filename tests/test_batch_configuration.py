from pathlib import Path

import pytest
from great_ai import GreatAI, ParallelTinyDbDriver, RouteConfig, configure
from great_ai.context import get_context


def test_spawn_batch_uses_parent_configuration(
    isolated_context: None, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    database = tmp_path / "custom-traces.json"
    monkeypatch.setattr(ParallelTinyDbDriver, "path_to_db", database)
    configure(
        prediction_cache_size=7,
        disable_se4ml_banner=True,
        route_config=RouteConfig(dashboard_enabled=False),
    )

    @GreatAI.create
    def predict(value: int) -> int:
        return get_context().prediction_cache_size + value

    monkeypatch.setattr("multiprocessing.get_all_start_methods", lambda: ["spawn"])
    assert [t.output for t in predict.process_batch([1, 2], concurrency=1)] == [8, 9]
    assert database.exists()
    assert len(get_context().tracing_database.query()[0]) == 2
