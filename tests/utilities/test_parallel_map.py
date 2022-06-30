import unittest

import pytest

from src.great_ai.utilities import parallel_map

COUNT = int(1e5) + 3


class TestParallelMap(unittest.TestCase):
    def test_simple_case_with_progress_bar(self) -> None:
        inputs = range(COUNT)
        expected = [v**2 for v in range(COUNT)]

        assert list(parallel_map(lambda v: v**2, inputs, concurrency=10)) == expected

    def test_with_iterable(self) -> None:
        from time import sleep

        def my_generator():
            for i in range(10):
                yield i
                sleep(0.1)

        expected = [v**3 for v in range(10)]

        assert (
            list(parallel_map(lambda x: x**3, my_generator(), chunk_size=1))
            == expected
        )

    def test_simple_case_without_progress_bar(self) -> None:
        inputs = range(COUNT)
        expected = [v**2 for v in range(COUNT)]

        assert (
            list(parallel_map(lambda v: v**2, inputs, disable_logging=True))
            == expected
        )

    def test_simple_case_invalid_values(self) -> None:
        inputs = range(COUNT)

        with pytest.raises(AssertionError):
            list(parallel_map(lambda v: v**2, inputs, concurrency=0))

        with pytest.raises(AssertionError):
            list(parallel_map(lambda v: v**2, inputs, chunk_size=0))

    def test_no_op(self) -> None:
        assert list(parallel_map(lambda v: v**2, [], disable_logging=True)) == []

        assert (
            list(
                parallel_map(lambda v: v**2, [], disable_logging=True, chunk_size=100)
            )
            == []
        )
        assert (
            list(
                parallel_map(
                    lambda v: v**2, [], disable_logging=True, concurrency=100
                )
            )
            == []
        )
