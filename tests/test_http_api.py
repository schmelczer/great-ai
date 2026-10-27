from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from great_ai import GreatAI, Trace, configure, context
from great_ai.deploy.routes.dashboard.create_dash_app import update_charts


@pytest.mark.parametrize("is_async", [False, True])
def test_service(
    is_async: bool, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(context, "_context", None)
    configure(version="1.2.3", disable_se4ml_banner=True)

    def predict_sync(value: int) -> int:
        return value + 2

    async def predict_async(value: int) -> int:
        return value + 2

    service = GreatAI.create(predict_async if is_async else predict_sync)

    with TestClient(service.app) as client:
        response = client.post("/predict", json={"value": 3})
        assert response.status_code == 200
        trace = response.json()
        assert trace["output"] == 5
        assert trace["logged_values"]["arg:value:value"] == 3

        trace_url = f"/traces/{trace['trace_id']}"
        assert client.get(trace_url).json() == trace
        assert client.post("/traces", json={}).json() == [trace]
        assert client.post("/predict", json={"value": "invalid"}).status_code == 422

        feedback_url = f"{trace_url}/feedback/"
        assert client.put(feedback_url, json={"feedback": "correct"}).status_code == 202
        assert client.get(feedback_url).json() == "correct"
        assert client.delete(feedback_url).status_code == 204
        assert client.get(feedback_url).json() is None

        health = client.get("/health")
        assert health.status_code == 200
        assert health.json()["is_healthy"] is True
        assert client.get("/version").json()["version"].split("+")[0] == "1.2.3"
        assert client.get("/openapi.json").status_code == 200
        assert client.get("/docs").status_code == 200
        assert client.get("/dashboard/").status_code == 200
        assert client.get("/dashboard/_dash-layout").status_code == 200
        assert client.get("/assets/index.css").status_code == 200

        histogram, coordinates, style = update_charts(
            [Trace.model_validate(trace)], accent_color="#123456"
        )
        assert len(histogram.figure.data) == 1
        assert len(coordinates.data) == 1
        assert style == {}

        assert client.delete(trace_url).status_code == 204
        assert client.get(trace_url).status_code == 404
