from asyncio import sleep

import pytest
from great_ai import GreatAI


def test_process_batch() -> None:
    @GreatAI.create
    def f(x: int) -> int:
        return x + 2

    assert [v.output for v in f.process_batch([3, 9, 34])] == [5, 11, 36]


@pytest.mark.asyncio
async def test_process_batch_async() -> None:
    @GreatAI.create
    async def f(x: int) -> int:
        await sleep(0.2)
        return x + 2

    assert [v.output for v in f.process_batch([3, 9, 34])] == [5, 11, 36]
