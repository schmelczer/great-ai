import re

from good_ai.utilities.clean import clean
from good_ai.utilities.lemmatize_text import lemmatize_text


def preprocess(text: str) -> str:
    lemmas = [re.sub(r"\d+", "NUM", lemma) for lemma in lemmatize_text(text)]
    return " ".join(lemmas)
