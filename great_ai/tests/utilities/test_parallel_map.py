import unittest

from src.great_ai.utilities.parallel_map import parallel_map

COUNT = int(1e5) + 3


class TestParallelMap(unittest.TestCase):
    def test_simple_case_with_progress_bar(self) -> None:
        inputs = range(COUNT)
        expected = [v**2 for v in range(COUNT)]

        assert parallel_map(lambda v: v**2, inputs) == expected

    def test_simple_case_without_progress_bar(self) -> None:
        inputs = range(COUNT)
        expected = [v**2 for v in range(COUNT)]

        self.assertEqual(
            parallel_map(lambda v: v**2, inputs, disable_progress=True), expected
        )

    def test_simple_case_invalid_values(self) -> None:
        inputs = range(COUNT)

        self.assertRaises(
            AssertionError, parallel_map, lambda v: v**2, inputs, concurrency=0
        )
        self.assertRaises(
            AssertionError, parallel_map, lambda v: v**2, inputs, chunk_size=0
        )

    def test_no_op(self) -> None:
        assert parallel_map(lambda v: v**2, [], disable_progress=True) == []
        self.assertEqual(
            parallel_map(lambda v: v**2, [], disable_progress=True, chunk_size=100),
            [],
        )
        self.assertEqual(
            parallel_map(lambda v: v**2, [], disable_progress=True, concurrency=100),
            [],
        )
