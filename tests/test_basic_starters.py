from functools import lru_cache

import pytest
from great_ai import (
    ArgumentValidationError,
    GreatAI,
    WrongDecoratorOrderError,
    parameter,
)


def test_create_trivial_cases() -> None:
    @GreatAI.create
    def hello_world_1(name: str) -> str:
        return f"Hello {name}!"

    assert hello_world_1("andras").output == "Hello andras!"

    @GreatAI.create
    def hello_world_2(name):  # type: ignore
        return f"Hello {name}!"

    assert hello_world_2("andras").output == "Hello andras!"


def test_create_with_other_decorator() -> None:
    @GreatAI.create
    @lru_cache
    def hello_world_1(name: str) -> str:
        return f"Hello {name}!"

    assert hello_world_1("andras").output == "Hello andras!"

    @lru_cache
    @GreatAI.create
    def hello_world_2(name: str) -> str:
        return f"Hello {name}!"

    assert hello_world_2("andras").output == "Hello andras!"


def test_with_parameter() -> None:
    @GreatAI.create
    @parameter("name", validate=lambda v: len(v) > 5)
    def hello_world(name: str) -> str:
        return f"Hello {name}!"

    assert hello_world("andras").output == "Hello andras!"

    with pytest.raises(ArgumentValidationError):
        hello_world("short")


def test_wrong_order() -> None:
    with pytest.raises(WrongDecoratorOrderError):

        @parameter("name", validate=lambda v: len(v) > 5)
        @GreatAI.create
        def hello_world(name: str) -> str:
            return f"Hello {name}!"
