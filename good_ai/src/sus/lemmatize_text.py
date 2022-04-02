from typing import List

from .lemmatize_token import lemmatize_token
from .nlp import nlp


def lemmatize_text(
    text: str,
    add_negation: bool = False,
    add_part_of_speech: bool = False,
) -> List[str]:
    doc = nlp(text)

    return [
        lemmatize_token(
            t,
            add_negation=add_negation,
            add_part_of_speech=add_part_of_speech,
        )
        for t in doc
    ]
