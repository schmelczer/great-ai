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
    """Return the list of sentences found in the input text.

    Use [syntok](https://github.com/fnl/syntok) to segment the sentences. Further
    processing can be enabled with optional arguments.

    Examples:
        >>> get_sentences('This is a sentence. This is a half')
        ['This is a sentence.', 'This is a half']

        >>> get_sentences('This is a sentence. This is a half', ignore_partial=True)
        ['This is a sentence.']

        >>> get_sentences('I like Apple.', true_case=True, remove_punctuation=True)
        ['i like Apple']

    Args:
        text: Text to be segmented into sentences.
        ignore_partial: Filter out sentences that are not capitalised/don't end with a
            punctuation.
        true_case: Crude method: lowercase the first word of each sentence.
        remove_punctuation: Remove all kinds of punctuation.

    Returns:
        The found sentences (with partial sentences optionally filtered out).
    """

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
