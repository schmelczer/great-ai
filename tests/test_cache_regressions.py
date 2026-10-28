import asyncio
from typing import Any, Dict, List, Tuple

import pytest
from fastapi.testclient import TestClient
from great_ai import GreatAI
from great_ai.context import get_context


def test_nested_tuple_inputs_can_be_cached(isolated_context: None) -> None:
    calls = 0

    @GreatAI.create
    def predict(value: Tuple[Dict[str, int]]) -> int:
        nonlocal calls
        calls += 1
        return value[0]["x"]

    assert predict(({"x": 7},)).output == 7
    assert predict(({"x": 7},)).output == 7
    assert calls == 1


@pytest.mark.asyncio
@pytest.mark.parametrize("cancelled", [False, True])
async def test_async_predictions_retry_after_failure(
    isolated_context: None, cancelled: bool
) -> None:
    calls = 0

    @GreatAI.create
    async def predict(value: int) -> int:
        nonlocal calls
        calls += 1
        if calls == 1:
            if cancelled:
                raise asyncio.CancelledError()
            raise ValueError("temporary failure")
        return value

    with pytest.raises(asyncio.CancelledError if cancelled else ValueError):
        await predict(7)
    assert (await predict(7)).output == 7
    assert (await predict(7)).output == 7
    assert calls == 2


def test_prediction_mutation_does_not_change_cache_keys(isolated_context: None) -> None:
    calls = 0

    @GreatAI.create
    def predict(values: List[int]) -> int:
        nonlocal calls
        calls += 1
        values.append(1)
        return len(values)

    original: List[int] = []
    assert predict(original).output == 1
    assert predict([]).output == 1
    assert original == []
    assert calls == 1


def test_caller_mutation_does_not_change_cached_trace_values(
    isolated_context: None,
) -> None:
    @GreatAI.create
    def predict(values: List[List[int]]) -> int:
        return values[0][0]

    original = [[1]]
    first = predict(original)
    original[0][0] = 2
    assert predict(original).output == 2
    assert predict([[1]]).trace_id == first.trace_id
    assert first.logged_values["arg:values:value"] == [[1]]


@pytest.mark.asyncio
@pytest.mark.parametrize("is_async", [False, True])
@pytest.mark.parametrize("do_not_persist", [False, True])
async def test_returned_traces_cannot_mutate_cached_results(
    isolated_context: None, is_async: bool, do_not_persist: bool
) -> None:
    calls = 0

    def predict(values: List[int]) -> List[List[int]]:
        nonlocal calls
        calls += 1
        return [values]

    async def predict_async(values: List[int]) -> List[List[int]]:
        return predict(values)

    service: Any = GreatAI.create(predict_async if is_async else predict)
    first = service([1], do_not_persist_traces=do_not_persist)
    if is_async:
        first = await first
    trace_id = first.trace_id
    first.output[0].append(99)
    first.logged_values["arg:values:value"].append(88)
    first.tags.append("changed")
    first.trace_id = "changed"
    first.feedback = "changed"

    second = service([1], do_not_persist_traces=do_not_persist)
    if is_async:
        second = await second
    assert second.trace_id == trace_id
    assert second.output == [[1]]
    assert second.logged_values["arg:values:value"] == [1]
    assert "changed" not in second.tags
    assert second.feedback is None
    assert calls == 1
    stored = get_context().tracing_database.get(trace_id)
    if do_not_persist:
        assert stored is None
    else:
        assert stored is not None
        assert stored.output == [[1]]


@pytest.mark.parametrize("is_async", [False, True])
def test_cached_predictions_follow_http_feedback_and_deletion(
    isolated_context: None, is_async: bool
) -> None:
    calls = 0

    def predict(value: int) -> int:
        nonlocal calls
        calls += 1
        return value * 2

    async def predict_async(value: int) -> int:
        return predict(value)

    service: Any = GreatAI.create(predict_async if is_async else predict)
    with TestClient(service.app) as client:
        first = client.post("/predict", json={"value": 2}).json()
        trace_url = f"/traces/{first['trace_id']}"
        feedback_url = f"{trace_url}/feedback/"
        assert (
            client.put(
                feedback_url, json={"feedback": {"label": "correct"}}
            ).status_code
            == 202
        )
        second = client.post("/predict", json={"value": 2}).json()
        assert second["trace_id"] == first["trace_id"]
        assert second["feedback"] == {"label": "correct"}
        assert second == client.get(trace_url).json()
        assert calls == 1
        assert client.delete(feedback_url).status_code == 204
        assert client.post("/predict", json={"value": 2}).json()["feedback"] is None
        assert client.delete(trace_url).status_code == 204
        third = client.post("/predict", json={"value": 2}).json()
        assert third["trace_id"] != first["trace_id"]
        assert third["output"] == 4
        assert calls == 2
        assert client.get(f"/traces/{third['trace_id']}").json() == third
        assert (
            client.put(
                f"/traces/{third['trace_id']}/feedback/", json={"feedback": "correct"}
            ).status_code
            == 202
        )


@pytest.mark.asyncio
@pytest.mark.parametrize("is_async", [False, True])
async def test_cached_predictions_observe_direct_database_changes(
    isolated_context: None, is_async: bool
) -> None:
    def predict(value: int) -> int:
        return value

    async def predict_async(value: int) -> int:
        return value

    service: Any = GreatAI.create(predict_async if is_async else predict)
    first = service(1)
    if is_async:
        first = await first
    database = get_context().tracing_database
    stored = database.get(first.trace_id)
    assert stored is not None
    stored.feedback = ["updated outside the service"]
    database.update(first.trace_id, stored)
    second = service(1)
    if is_async:
        second = await second
    assert second.feedback == stored.feedback
    second.feedback.append("caller change")
    database.delete(first.trace_id)
    third = service(1)
    if is_async:
        third = await third
    assert third.trace_id != first.trace_id
    assert database.get(third.trace_id) is not None
