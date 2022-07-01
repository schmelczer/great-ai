import unittest

import pytest

from src.great_ai.utilities import parallel_map

COUNT = int(1e5) + 3


class TestParallelMap(unittest.TestCase):
    def test_simple_case_with_progress_bar(self) -> None:
        assert list(parallel_map(lambda v: v**2, range(COUNT), concurrency=4)) == [
            v**2 for v in range(COUNT)
        ]

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
        assert list(
            parallel_map(
                lambda v: v**2, range(COUNT), disable_logging=True, concurrency=2
            )
        ) == [v**2 for v in range(COUNT)]

    def test_simple_case_invalid_values(self) -> None:
        with pytest.raises(AssertionError):
            list(parallel_map(lambda v: v**2, range(COUNT), concurrency=0))

        with pytest.raises(AssertionError):
            list(parallel_map(lambda v: v**2, range(COUNT), chunk_size=0))

    def test_this_process_exception(self) -> None:
        def my_generator():
            yield 1
            yield 2
            yield 3
            assert False

        with pytest.raises(AssertionError):
            list(
                parallel_map(
                    lambda v: v**2, my_generator(), concurrency=2, chunk_size=2
                )
            )

        with pytest.raises(AssertionError):
            list(
                parallel_map(
                    lambda v: v**2, my_generator(), concurrency=1, chunk_size=2
                )
            )

    def test_ignore_this_process_exception(self) -> None:
        def my_generator():
            yield 1
            yield 2
            yield 3
            yield 1 / 0

        assert list(
            parallel_map(
                lambda v: v**2,
                my_generator(),
                concurrency=2,
                chunk_size=2,
                ignore_exceptions=True,
            )
        ) == [1, 4]
        assert list(
            parallel_map(
                lambda v: v**2,
                my_generator(),
                concurrency=1,
                chunk_size=2,
                ignore_exceptions=True,
            )
        ) == [1, 4, 9]

    def test_worker_process_exception(self) -> None:
        def oh_no(_):
            raise ValueError("hi")

        with pytest.raises(ValueError):
            list(parallel_map(oh_no, range(COUNT), concurrency=2))

        with pytest.raises(ValueError):
            list(parallel_map(oh_no, range(COUNT), concurrency=1))

    def test_ignore_worker_process_exception(self) -> None:
        def oh_no(_):
            raise ValueError("hi")

        assert (
            list(parallel_map(oh_no, range(3), concurrency=2, ignore_exceptions=True))
            == [None] * 3
        )
        assert (
            list(parallel_map(oh_no, range(3), concurrency=1, ignore_exceptions=True))
            == [None] * 3
        )

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
