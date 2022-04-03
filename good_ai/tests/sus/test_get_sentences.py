import unittest

from src.good_ai.utilities.get_sentences import get_sentences


class TestGetSentences(unittest.TestCase):
    def test_default(self) -> None:
        text = "This is a complete sentence. So is this. However this is n"  # ot.
        expected = ["This is a complete sentence.", "So is this.", "However this is n"]

        self.assertEqual(get_sentences(text), expected)
        self.assertEqual(get_sentences(text, ignore_partial=True), expected[0:2])

    def test_empty(self) -> None:
        self.assertEqual(get_sentences(""), [])
        self.assertEqual(get_sentences("", ignore_partial=True), [])
