import unittest

from src.great_ai.utilities import lemmatize_token, nlp


class TestLemmatizeToken(unittest.TestCase):
    def test_simple(self) -> None:
        token = nlp("Center")[0]

        assert lemmatize_token(token) == "centre"
        assert lemmatize_token(token, add_negation=True) == "centre"
        assert lemmatize_token(token, add_part_of_speech=True) == "centre_NOUN"

    def test_punctuation(self) -> None:
        token = nlp("This.")[1]

        assert lemmatize_token(token) == "."
        assert lemmatize_token(token, add_negation=True) == "."
        assert lemmatize_token(token, add_part_of_speech=True) == "._PUNCT"
