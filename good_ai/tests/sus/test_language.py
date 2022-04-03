import unittest

from src.good_ai.utilities.language import (
    english_name_of_language,
    is_english,
    predict_language,
)


class TestLanguage(unittest.TestCase):
    def test_predict_language(self) -> None:
        self.assertEqual(predict_language("This is an English text."), "en")
        self.assertEqual(predict_language("Ez egy magyar szöveg."), "hu")
        self.assertEqual(predict_language("此處按原典，應為「黃武元年」，而電子稿此處為「黃初元年」。"), "zh-TW")
        self.assertEqual(predict_language("32"), "und")
        self.assertEqual(predict_language(""), "und")

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
        self.assertEqual(english_name_of_language("en"), "English")
        self.assertEqual(english_name_of_language("hu"), "Hungarian")
        self.assertEqual(english_name_of_language("zh"), "Chinese")
        self.assertEqual(english_name_of_language("zh-TW"), "Chinese")
        self.assertEqual(english_name_of_language("und"), "Unknown language")
        self.assertEqual(english_name_of_language(""), "Unknown language")
        self.assertEqual(english_name_of_language(None), "Unknown language")
