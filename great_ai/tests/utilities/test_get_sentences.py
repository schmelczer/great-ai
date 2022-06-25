import unittest

from src.great_ai.utilities import get_sentences


class TestGetSentences(unittest.TestCase):
    def test_default(self) -> None:
        text = "This is a complete sentence. So is this. However this is n"  # ot.
        expected = ["This is a complete sentence.", "So is this.", "However this is n"]

        assert get_sentences(text) == expected
        assert get_sentences(text, ignore_partial=True) == expected[0:2]

    def test_empty(self) -> None:
        assert get_sentences("") == []
        assert get_sentences("", ignore_partial=True) == []
