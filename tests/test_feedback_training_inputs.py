from typing import Any, Dict

from fastapi.testclient import TestClient
from great_ai import (
    GreatAI,
    Trace,
    add_ground_truth,
    log_metric,
    parameter,
    query_ground_truth,
    save_model,
    use_model,
)


def test_uploaded_and_online_feedback_share_training_input_shape(
    isolated_context: None,
) -> None:
    @GreatAI.create
    def predict(text: str) -> str:
        log_metric("length", len(text))
        return text.upper()

    add_ground_truth(["dog"], ["DOG"])
    with TestClient(predict.app) as client:
        trace = client.post("/predict", json={"text": "cat"}).json()
        client.put(f"/traces/{trace['trace_id']}/feedback/", json={"feedback": "CAT"})
    pairs = {(trace.input, trace.feedback) for trace in query_ground_truth()}
    assert pairs == {("cat", "CAT"), ("dog", "DOG")}


def test_dictionary_inputs_remain_dictionaries(isolated_context: None) -> None:
    @GreatAI.create
    def predict(data: Dict[str, Any]) -> int:
        return len(data)

    original = {"input": {"nested": [1, 2]}}
    add_ground_truth([original], [1], tags="online")
    with TestClient(predict.app) as client:
        trace = client.post("/predict", json={"data": original}).json()
        client.put(f"/traces/{trace['trace_id']}/feedback/", json={"feedback": 1})
    data = query_ground_truth()
    assert len(data) == 2
    assert all(trace.input == original for trace in data)


def test_multi_argument_inputs_exclude_models_metrics_and_private_arguments(
    isolated_context: None,
) -> None:
    save_model(3, "constant")

    @GreatAI.create
    @parameter("secret", disable_logging=True)
    @use_model("constant")
    def predict(text: str, model: int, *, secret: str, count: int = 2) -> str:
        log_metric("custom", model)
        return text * count

    original = {"text": "cat", "count": 2}
    add_ground_truth([original], ["catcat"])
    with TestClient(predict.app) as client:
        trace = client.post(
            "/predict", json={"text": "cat", "secret": "private"}
        ).json()
        client.put(
            f"/traces/{trace['trace_id']}/feedback/", json={"feedback": "catcat"}
        )
    assert all(trace.input == original for trace in query_ground_truth())
    assert "private" not in str(query_ground_truth())


def test_legacy_uploaded_dictionary_and_online_traces_remain_readable() -> None:
    base: Dict[str, Any] = dict(
        trace_id="old", created="2022-01-01", original_execution_time_ms=0, models=[]
    )
    uploaded = Trace(
        **base, logged_values={"text": "cat", "count": 2}, tags=["ground_truth"]
    )
    assert uploaded.input == {"text": "cat", "count": 2}
    online = Trace(
        **base,
        logged_values={
            "arg:text:value": "cat",
            "arg:text:length": 3,
            "metric:predict:custom": 1,
        },
        tags=["online"],
    )
    assert online.input == "cat"
