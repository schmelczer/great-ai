from asyncio import sleep

import pytest

from great_ai import (
    ArgumentValidationError,
    GreatAI,
    WrongDecoratorOrderError,
    parameter,
)


@pytest.mark.asyncio
async def test_create_trivial_cases() -> None:
    @GreatAI.create
    async def hello_world_1(name: str) -> str:
        await sleep(0.5)
        return f"Hello {name}!"

    assert (await hello_world_1("andras").output) == "Hello andras!"

    @GreatAI.create
    async def hello_world_2(name: str) -> str:
        await sleep(0.5)
        return f"Hello {name}!"

    assert (await hello_world_2("andras").output) == "Hello andras!"

    @GreatAI.create()
    async def hello_world_3(name: str) -> str:
        await sleep(0.5)
        return f"Hello {name}!"

    assert (await hello_world_3("andras").output) == "Hello andras!"

    @GreatAI.create()
    async def hello_world_4(name):
        await sleep(0.5)
        return f"Hello {name}!"

    assert (await hello_world_4("andras").output) == "Hello andras!"


@pytest.mark.asyncio
async def test_with_parameter() -> None:
    @GreatAI.create
    @parameter("name", validator=lambda v: len(v) > 5)
    async def hello_world(name: str) -> str:
        await sleep(0.5)
        return f"Hello {name}!"

    assert (await hello_world("andras").output) == "Hello andras!"

    with pytest.raises(ArgumentValidationError):
        await hello_world("short")

    with pytest.raises(WrongDecoratorOrderError):

        @parameter("name", validator=lambda v: len(v) > 5)
        @GreatAI.create
        def hello_world(name: str) -> str:
            return f"Hello {name}!"
