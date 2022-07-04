import unittest
from functools import lru_cache

import pytest

from great_ai import (
    ArgumentValidationError,
    GreatAI,
    WrongDecoratorOrderError,
    parameter,
)


class TestHumanReadableToByte(unittest.TestCase):
    def test_create_simple_cases(self) -> None:
        @GreatAI.create
        def hello_world(name: str) -> str:
            return f"Hello {name}!"

        assert hello_world("andras").output == "Hello andras!"

        @GreatAI.create
        def hello_world(name):
            return f"Hello {name}!"

        assert hello_world("andras").output == "Hello andras!"

        @GreatAI.create()
        def hello_world(name: str) -> str:
            return f"Hello {name}!"

        assert hello_world("andras").output == "Hello andras!"

    def test_create_with_other_decorator(self) -> None:
        @GreatAI.create
        @lru_cache
        def hello_world(name: str) -> str:
            return f"Hello {name}!"

        assert hello_world("andras").output == "Hello andras!"

        @lru_cache
        @GreatAI.create()
        def hello_world(name: str) -> str:
            return f"Hello {name}!"

        assert hello_world("andras").output == "Hello andras!"

    def test_with_parameter(self) -> None:
        @GreatAI.create
        @parameter("name", validator=lambda v: len(v) > 5)
        def hello_world(name: str) -> str:
            return f"Hello {name}!"

        assert hello_world("andras").output == "Hello andras!"

        with pytest.raises(ArgumentValidationError):
            hello_world("short")

        with pytest.raises(WrongDecoratorOrderError):

            @parameter("name", validator=lambda v: len(v) > 5)
            @GreatAI.create
            def hello_world(name: str) -> str:
                return f"Hello {name}!"
