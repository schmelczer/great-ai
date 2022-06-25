import unittest

from src.great_ai.utilities.lemmatize_text import lemmatize_text


class TestLemmatizeText(unittest.TestCase):
    def test_simple(self) -> None:
        text = "The state-of-the-art could not be improved, however we managed to create a less resource-intensive implementation of it."

        lemmatized = [
            "the",
            "state",
            "-",
            "of",
            "-",
            "the",
            "-",
            "art",
            "could",
            "not",
            "be",
            "improve",
            ",",
            "however",
            "we",
            "manage",
            "to",
            "create",
            "a",
            "less",
            "resource",
            "-",
            "intensive",
            "implementation",
            "of",
            "it",
            ".",
        ]

        lemmatized_pos = [
            "the_DET",
            "state_NOUN",
            "-_PUNCT",
            "of_ADP",
            "-_PUNCT",
            "the_DET",
            "-_PUNCT",
            "art_NOUN",
            "could_AUX",
            "not_PART",
            "be_AUX",
            "improve_VERB",
            ",_PUNCT",
            "however_ADV",
            "we_PRON",
            "manage_VERB",
            "to_PART",
            "create_VERB",
            "a_DET",
            "less_ADV",
            "resource_NOUN",
            "-_PUNCT",
            "intensive_ADJ",
            "implementation_NOUN",
            "of_ADP",
            "it_PRON",
            "._PUNCT",
        ]

        lemmatized_neg = [
            "the",
            "state",
            "-",
            "of",
            "-",
            "the",
            "-",
            "art",
            "could",
            "not",
            "NOT_be",
            "NOT_improve",
            "NOT_,",
            "however",
            "we",
            "manage",
            "to",
            "create",
            "a",
            "less",
            "resource",
            "-",
            "intensive",
            "implementation",
            "of",
            "it",
            ".",
        ]

        lemmatized_pos_neg = [
            "the_DET",
            "state_NOUN",
            "-_PUNCT",
            "of_ADP",
            "-_PUNCT",
            "the_DET",
            "-_PUNCT",
            "art_NOUN",
            "could_AUX",
            "not_PART",
            "NOT_be_AUX",
            "NOT_improve_VERB",
            "NOT_,_PUNCT",
            "however_ADV",
            "we_PRON",
            "manage_VERB",
            "to_PART",
            "create_VERB",
            "a_DET",
            "less_ADV",
            "resource_NOUN",
            "-_PUNCT",
            "intensive_ADJ",
            "implementation_NOUN",
            "of_ADP",
            "it_PRON",
            "._PUNCT",
        ]

        assert lemmatize_text(text) == lemmatized
        assert lemmatize_text(text, add_part_of_speech=True) == lemmatized_pos
        assert lemmatize_text(text, add_negation=True) == lemmatized_neg
        self.assertEqual(
            lemmatize_text(text, add_negation=True, add_part_of_speech=True),
            lemmatized_pos_neg,
        )

    def test_empty(self) -> None:
        assert lemmatize_text("") == []
