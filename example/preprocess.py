import re

from great_ai.utilities.lemmatize_text import lemmatize_text


def preprocess(text: str) -> str:
    lemmas = [re.sub(r"\d[\d.,]*", "NUM", lemma) for lemma in lemmatize_text(text)]
    return " ".join(lemmas)
