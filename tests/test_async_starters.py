from asyncio import sleep

import pytest
from great_ai import GreatAI, WrongDecoratorOrderError, parameter


@pytest.mark.asyncio
async def test_create_trivial_cases() -> None:
    @GreatAI.create
    async def hello_world_1(name: str) -> str:
        await sleep(0.5)
        return f"Hello {name}!"

    assert (await hello_world_1("andras")).output == "Hello andras!"

    @GreatAI.create
    async def hello_world_2(name: str) -> str:
        await sleep(0.5)
        return f"Hello {name}!"

    assert (await hello_world_2("andras")).output == "Hello andras!"


@pytest.mark.asyncio
async def test_with_parameter() -> None:
    @GreatAI.create
    @parameter("name", validate=lambda v: len(v) > 5)
    async def hello_world(name: str) -> str:
        await sleep(0.5)
        return f"Hello {name}!"


@pytest.mark.asyncio
async def test_with_parameters() -> None:
    @GreatAI.create
    @parameter("name", validate=lambda v: len(v) > 5)
    @parameter("unused", disable_logging=True)
    async def hello_world(name: str, unused) -> str:  # type: ignore
        await sleep(0.5)
        return f"Hello {name}!"

    assert (await hello_world("andras", "fr")).output == "Hello andras!"


def test_wrong_order() -> None:
    with pytest.raises(WrongDecoratorOrderError):

        @parameter("name", validate=lambda v: len(v) > 5)
        @GreatAI.create
        async def hello_world(name: str) -> str:
            return f"Hello {name}!"
