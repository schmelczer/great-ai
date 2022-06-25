import unittest
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # don't show a window for each test

from src.great_ai.utilities import evaluate_ranking


class TestEvaluateRanking(unittest.TestCase):
    def test_default(self) -> None:
        results = evaluate_ranking(
            ["a", "a", "b", "b", "c", "d", "d", "d"],
            [10, 7, 11, 6, 8, 2, 7, 1],
            target_recall=0.6,
            reverse_order=True,
        )

        self.assertEqual(
            results,
            {"d": 1.0, "c": 0.6666666666666666, "b": 0.4},
        )

        results = evaluate_ranking(
            ["a", "a", "b", "b", "c", "d", "d", "d"],
            [10, 7, 11, 6, 8, 2, 7, 1],
            target_recall=0.6,
            reverse_order=False,
            disable_interpolation=True,
        )

        self.assertEqual(
            results,
            {"a": 0.6666666666666666, "b": 0.3333333333333333, "c": 0.2857142857142857},
        )

    def test_mismatching_lengths(self) -> None:
        self.assertRaises(
            ValueError,
            evaluate_ranking,
            ["a", "a", "b", "b", "c"],
            [10, 7, 11, 6, 8, 2, 7, 1],
            target_recall=0.6,
        )

    def test_invalid_recalls(self) -> None:
        self.assertRaises(
            AssertionError,
            evaluate_ranking,
            ["a", "a", "b", "b"],
            [10, 7, 11, 6],
            target_recall=10.6,
        )

        self.assertRaises(
            AssertionError,
            evaluate_ranking,
            ["a", "a", "b", "b"],
            [10, 7, 11, 6],
            target_recall=-0.0001,
        )

        self.assertRaises(
            AssertionError,
            evaluate_ranking,
            ["a", "a", "b", "b"],
            [10, 7, 11, 6],
            target_recall=1.00001,
        )

    def test_empty(self) -> None:
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

    def test_save(self) -> None:
        path = Path("test.svg")
        path.unlink(missing_ok=True)

        evaluate_ranking(
            ["a", "a", "b", "b", "c", "d", "d", "d"],
            [10, 7, 11, 6, 8, 2, 7, 1],
            target_recall=0.1,
            output_svg=path,
        )

        self.assertTrue(path.exists())
        path.unlink()
