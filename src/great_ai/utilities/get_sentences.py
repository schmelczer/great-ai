from typing import List, cast

from segtok.segmenter import split_multi

from .data import sentence_ending_punctuations


def get_sentences(
    text: str, ignore_partial: bool = False, true_case: bool = False
) -> List[str]:
    if text.strip() == "":
        return []

    possible_sentences = [
        cast(str, s).strip() for s in split_multi(text) if cast(str, s).strip()
    ]

    if ignore_partial:
        possible_sentences = [
            s
            for s in possible_sentences
            if s[0].isupper() and s[-1] in sentence_ending_punctuations
        ]

    if true_case:
        possible_sentences = [
            s[0].lower() + s[1:] for s in possible_sentences  # very crude method
        ]

    return possible_sentences
