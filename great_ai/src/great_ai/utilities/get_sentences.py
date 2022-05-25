from typing import List

from segtok.segmenter import split_multi

from .data import sentence_ending_punctuations


def get_sentences(text: str, ignore_partial: bool = False) -> List[str]:
    if text.strip() == "":
        return []

    possible_sentences = [s for s in split_multi(text) if s]

    if ignore_partial:
        possible_sentences = [
            s
            for s in possible_sentences
            if s[0].isupper() and s[-1] in sentence_ending_punctuations
        ]

    return possible_sentences
