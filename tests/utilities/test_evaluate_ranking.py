from pathlib import Path

import matplotlib
import pytest

matplotlib.use("Agg")  # don't show a window for each test

from great_ai.utilities import evaluate_ranking


def test_default() -> None:
    results = evaluate_ranking(
        ["a", "a", "b", "b", "c", "d", "d", "d"],
        [10, 7, 11, 6, 8, 2, 7, 1],
        target_recall=0.6,
        reverse_order=True,
    )

    assert results == {"d": 5 / 6, "c": 2 / 3, "b": 2 / 5}

    results = evaluate_ranking(
        ["a", "a", "b", "b", "c", "d", "d", "d"],
        [10, 7, 11, 6, 8, 2, 7, 1],
        target_recall=0.6,
        reverse_order=False,
        disable_interpolation=True,
    )

    assert results == {"a": 0.6, "b": 0.4, "c": 0.2}


def test_mismatching_lengths() -> None:
    with pytest.raises(ValueError):
        evaluate_ranking(
            ["a", "a", "b", "b", "c"],
            [10, 7, 11, 6, 8, 2, 7, 1],
            target_recall=0.6,
        )


def test_invalid_recalls() -> None:
    with pytest.raises(AssertionError):
        evaluate_ranking(
            ["a", "a", "b", "b"],
            [10, 7, 11, 6],
            target_recall=10.6,
        )

    with pytest.raises(AssertionError):
        evaluate_ranking(
            ["a", "a", "b", "b"],
            [10, 7, 11, 6],
            target_recall=-0.0001,
        )

    with pytest.raises(AssertionError):
        evaluate_ranking(
            ["a", "a", "b", "b"],
            [10, 7, 11, 6],
            target_recall=1.00001,
        )


def test_empty() -> None:
    evaluate_ranking(
        [],
        [],
        target_recall=0.6,
    )

    evaluate_ranking(
        ["a"],
        [1],
        target_recall=0.6,
    )


def test_save() -> None:
    path = Path("test.svg")
    try:
        path.unlink()
    except FileNotFoundError:
        # missing_ok only exists >= Python 3.8
        pass

    evaluate_ranking(
        ["a", "a", "b", "b", "c", "d", "d", "d"],
        [10, 7, 11, 6, 8, 2, 7, 1],
        target_recall=0.1,
        output_svg=path,
    )

    assert path.exists()
    path.unlink()
