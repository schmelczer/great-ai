import unittest

from src.great_ai.utilities.lemmatize_text import lemmatize_token
from src.great_ai.utilities.nlp import nlp


class TestLemmatizeToken(unittest.TestCase):
    def test_simple(self) -> None:
        token = nlp("Center")[0]

        self.assertEqual(lemmatize_token(token), "centre")
        self.assertEqual(lemmatize_token(token, add_negation=True), "centre")
        self.assertEqual(lemmatize_token(token, add_part_of_speech=True), "centre_NOUN")

    def test_punctuation(self) -> None:
        token = nlp("This.")[1]

        self.assertEqual(lemmatize_token(token), ".")
        self.assertEqual(lemmatize_token(token, add_negation=True), ".")
        self.assertEqual(lemmatize_token(token, add_part_of_speech=True), "._PUNCT")
