import pytest
from great_ai.utilities import chunk


def test_simple() -> None:
    i = [1, 2, 3, 4]

    assert list(chunk(i, 1)) == [[1], [2], [3], [4]]
    assert list(chunk(i, 2)) == [[1, 2], [3, 4]]
    assert list(chunk(i, 3)) == [[1, 2, 3], [4]]
    assert list(chunk(i, 4)) == [[1, 2, 3, 4]]
    assert list(chunk(i, 5)) == [[1, 2, 3, 4]]
    assert list(chunk(i, 125)) == [[1, 2, 3, 4]]


def test_bad_argument() -> None:
    with pytest.raises(AssertionError):
        list(chunk([], -10))

    with pytest.raises(AssertionError):
        list(chunk([], 0))


def test_generator() -> None:
    def my_generator():  # type: ignore
        for i in range(1, 11):
            yield i

    assert list(chunk(range(1, 11), 3)) == [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10]]
    assert list(chunk(my_generator(), 3)) == [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10]]
