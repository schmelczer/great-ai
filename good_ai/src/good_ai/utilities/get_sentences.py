from typing import List

from .data import sentence_ending_punctuations
from .nlp import nlp


def get_sentences(text: str, ignore_partial: bool = False) -> List[str]:
    doc = nlp(text)
    possible_sentences = [s.text for s in doc.sents]

    if ignore_partial:
        possible_sentences = [
            s
            for s in possible_sentences
            if s[0].isupper() and s[-1] in sentence_ending_punctuations
        ]

    return possible_sentences
