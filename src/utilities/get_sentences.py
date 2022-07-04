import re
from string import punctuation
from typing import List

from syntok.segmenter import segment
from syntok.tokenizer import Tokenizer

from .data import sentence_ending_punctuations

punctuations_pattern = re.compile(f"\\s*[{re.escape(punctuation)}]+\\s*")


def get_sentences(
    text: str,
    ignore_partial: bool = False,
    true_case: bool = False,
    remove_punctuation: bool = False,
) -> List[str]:
    tokenizer = Tokenizer(
        emit_hyphen_or_underscore_sep=True, replace_not_contraction=False
    )
    token_stream = tokenizer.tokenize(text)

    def process(sentence: str) -> str:
        if true_case:
            sentence = sentence[0].lower() + sentence[1:]  # very crude method
        if remove_punctuation:
            sentence = re.sub(punctuations_pattern, " ", sentence)
        return sentence.strip()

    sentences = [
        process(tokenizer.to_text(sentence)) for sentence in segment(token_stream)
    ]

    if ignore_partial:
        sentences = [
            sentence
            for sentence in sentences
            if sentence[0].isupper() and sentence[-1] in sentence_ending_punctuations
        ]

    return sentences
