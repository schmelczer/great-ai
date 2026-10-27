import asyncio
from typing import Dict, List, Tuple

import pytest
from great_ai import GreatAI


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
