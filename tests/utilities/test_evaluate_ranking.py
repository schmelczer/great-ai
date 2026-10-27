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

    assert results == {"d": 1.0, "c": 1.0, "b": 1 / 2}

    results = evaluate_ranking(
        ["a", "a", "b", "b", "c", "d", "d", "d"],
        [10, 7, 11, 6, 8, 2, 7, 1],
        target_recall=0.6,
        reverse_order=False,
        disable_interpolation=True,
    )

    assert results == {"a": 2 / 3, "b": 2 / 5, "c": 2 / 7}


@pytest.mark.parametrize("disable_interpolation", [False, True])
def test_perfect_ranking_at_full_recall(disable_interpolation: bool) -> None:
    assert evaluate_ranking(
        [1, 1, 0, 0],
        [4, 3, 2, 1],
        target_recall=1,
        disable_interpolation=disable_interpolation,
        plot=False,
    ) == {0: 1.0}


def test_tied_scores_cannot_be_separated_by_a_threshold() -> None:
    for labels in ([1, 0], [0, 1]):
        assert evaluate_ranking(labels, [1, 1], target_recall=1, plot=False) == {0: 0.5}


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
