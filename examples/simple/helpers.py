import re

from great_ai.utilities.clean import clean
from great_ai.utilities.lemmatize_text import lemmatize_text


def preprocess(text: str) -> str:
    text = clean(text, convert_to_ascii=True)
    text = re.sub(r"[^a-zA-Z0-9]", " ", text)
    return text


def lemmatize(text: str) -> str:
    lemmatized = lemmatize_text(text)
    clean_lemmas = [re.sub(r"\d[\d.,]*", "NUM", lemma) for lemma in lemmatized]
    return " ".join(clean_lemmas)
