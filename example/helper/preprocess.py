import re

from sus.clean import clean
from sus.lemmatize_text import lemmatize_text


def preprocess(text: str) -> str:
    cleaned = clean(text, convert_to_ascii=True)
    lemmas = [re.sub(r"\d+", "NUM", lemma) for lemma in lemmatize_text(cleaned)]
    return " ".join(lemmas)
