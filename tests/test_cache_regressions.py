import asyncio
from typing import Dict, Tuple

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
