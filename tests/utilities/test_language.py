import unittest

from src.great_ai.utilities import (
    english_name_of_language,
    is_english,
    predict_language,
)


class TestLanguage(unittest.TestCase):
    def test_predict_language(self) -> None:
        assert predict_language("This is an English text.") == "en"
        assert predict_language("Ez egy magyar szöveg.") == "hu"
        assert predict_language("32") == "und"
        assert predict_language("") == "und"

    def test_is_english(self) -> None:
        self.assertTrue(is_english("en"))
        self.assertTrue(is_english("en-US"))
        self.assertFalse(is_english("hu"))
        self.assertFalse(is_english("de"))
        self.assertFalse(is_english("zh"))
        self.assertFalse(is_english("zh-TW"))
        self.assertFalse(is_english("und"))
        self.assertFalse(is_english(""))
        self.assertFalse(is_english(None))

    def english_name_of_language(self) -> None:
        assert english_name_of_language("en") == "English"
        assert english_name_of_language("hu") == "Hungarian"
        assert english_name_of_language("zh") == "Chinese"
        assert english_name_of_language("zh-TW") == "Chinese"
        assert english_name_of_language("und") == "Unknown language"
        assert english_name_of_language("") == "Unknown language"
        assert english_name_of_language(None) == "Unknown language"
