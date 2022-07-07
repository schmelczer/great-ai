from typing import Any, Iterable

import pytest
from great_ai.utilities import WorkerException, threaded_parallel_map
from typing_extensions import Never

COUNT = int(1e5) + 3


def test_simple_case() -> None:
    assert list(
        threaded_parallel_map(lambda v: v**2, range(COUNT), concurrency=4)
    ) == [v**2 for v in range(COUNT)]


def test_with_iterable() -> None:
    from time import sleep

    def my_generator() -> Iterable[int]:
        for i in range(10):
            yield i
            sleep(0.1)

    expected = [v**3 for v in range(10)]

    assert (
        list(threaded_parallel_map(lambda x: x**3, my_generator(), chunk_size=1))
        == expected
    )


def test_simple_case_invalid_values() -> None:
    with pytest.raises(AssertionError):
        list(threaded_parallel_map(lambda v: v**2, range(COUNT), concurrency=0))

    with pytest.raises(AssertionError):
        list(threaded_parallel_map(lambda v: v**2, range(COUNT), chunk_size=0))


def test_this_worker_exception() -> None:
    def my_generator() -> Iterable[int]:
        yield 1
        yield 2
        yield 3
        assert False

    with pytest.raises(AssertionError):
        list(
            threaded_parallel_map(
                lambda v: v**2, my_generator(), concurrency=2, chunk_size=2
            )
        )

    with pytest.raises(AssertionError):
        list(
            threaded_parallel_map(
                lambda v: v**2, my_generator(), concurrency=1, chunk_size=2
            )
        )


def test_ignore_this_worker_exception() -> None:
    def my_generator() -> Iterable[float]:
        yield 1
        yield 2
        yield 3
        yield 1 / 0

    assert list(
        threaded_parallel_map(
            lambda v: v**2,
            my_generator(),
            concurrency=2,
            chunk_size=2,
            ignore_exceptions=True,
        )
    ) == [
        1,
        4,
    ]  # the second chunk is ruined because of the error


def test_worker_worker_exception() -> None:
    def oh_no(_: Any) -> Never:
        raise ValueError("hi")

    with pytest.raises(WorkerException):
        list(threaded_parallel_map(oh_no, range(COUNT), concurrency=2))

    with pytest.raises(WorkerException):
        list(threaded_parallel_map(oh_no, range(COUNT), concurrency=1))


def test_ignore_worker_worker_exception() -> None:
    def oh_no(_: Any) -> Never:
        raise ValueError("hi")

    assert (
        list(
            threaded_parallel_map(
                oh_no, range(3), concurrency=2, ignore_exceptions=True
            )
        )
        == [None] * 3
    )
    assert (
        list(
            threaded_parallel_map(
                oh_no, range(3), concurrency=1, ignore_exceptions=True
            )
        )
        == [None] * 3
    )


def test_no_op() -> None:
    assert list(threaded_parallel_map(lambda v: v**2, [])) == []
    assert list(threaded_parallel_map(lambda v: v**2, [], chunk_size=100)) == []
    assert list(threaded_parallel_map(lambda v: v**2, [], concurrency=100)) == []
