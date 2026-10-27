from datetime import datetime, timezone
from typing import Set

from fastapi.testclient import TestClient
from great_ai import GreatAI
from great_ai.context import get_context
from pydantic import BaseModel


class DatedInput(BaseModel):
    when: datetime
    tags: Set[int]


def test_tinydb_persists_json_compatible_model_values(isolated_context: None) -> None:
    @GreatAI.create
    def predict(data: DatedInput) -> int:
        return len(data.tags)

    with TestClient(predict.app) as client:
        response = client.post(
            "/predict", json={"data": {"when": "2026-01-01T00:00:00Z", "tags": [1, 2]}}
        )
        assert response.status_code == 200
        trace_id = response.json()["trace_id"]
    database = get_context().tracing_database
    trace = database.get(trace_id)
    assert trace is not None
    assert trace.output == 2
    trace.feedback = {"when": datetime(2026, 1, 1, tzinfo=timezone.utc)}
    database.update(trace_id, trace)
    updated = database.get(trace_id)
    assert updated is not None
    assert updated.feedback == {"when": "2026-01-01T00:00:00Z"}
    database.save_batch([trace.model_copy(update={"trace_id": "batch"})])
    assert database.get("batch") is not None
