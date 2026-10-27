import multiprocessing as mp
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from unittest.mock import patch

from tinydb.table import Table

from great_ai import ParallelTinyDbDriver, Trace
from great_ai.context import get_context


def write_traces(path: str, index: int, barrier: Any) -> None:
    ParallelTinyDbDriver.path_to_db = Path(path)
    read_table = Table._read_table

    def slow_read(self: Table) -> Any:
        data = read_table(self)
        time.sleep(0.02)
        return data

    barrier.wait(timeout=10)
    with patch.object(Table, "_read_table", slow_read):
        for i in range(3):
            ParallelTinyDbDriver().save(
                Trace(
                    trace_id=f"{index}-{i}",
                    created="2026-01-01",
                    original_execution_time_ms=0,
                    models=[],
                    tags=[],
                    logged_values={},
                )
            )


def test_spawned_writers_share_database_lock(tmp_path: Path) -> None:
    ctx = mp.get_context("spawn")
    path = tmp_path / "traces.json"
    barrier = ctx.Barrier(2)
    processes = [
        ctx.Process(target=write_traces, args=(str(path), i, barrier)) for i in range(2)
    ]
    try:
        for process in processes:
            process.start()
        for process in processes:
            process.join(timeout=15)
            assert process.exitcode == 0
    finally:
        for process in processes:
            if process.is_alive():
                process.kill()
                process.join()
            process.close()
    with patch.object(ParallelTinyDbDriver, "path_to_db", path):
        assert len(ParallelTinyDbDriver().query()[0]) == 6


def test_tinydb_date_queries_normalize_timezones(isolated_context: None) -> None:
    database = get_context().tracing_database
    for i, created in enumerate(("2026-01-01T12:00:00", "2026-01-01T14:00:00+02:00")):
        database.save(
            Trace(
                trace_id=str(i),
                created=created,
                original_execution_time_ms=0,
                models=[],
                tags=[],
                logged_values={},
            )
        )
    noon = datetime(2026, 1, 1, 12, tzinfo=timezone.utc)
    assert database.query(since=noon, until=noon)[1] == 2
    assert database.query(since=noon.replace(hour=13))[1] == 0
