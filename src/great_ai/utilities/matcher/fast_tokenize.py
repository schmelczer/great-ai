import re
from typing import List, Union

from segtok.tokenizer import word_tokenizer

from ..get_sentences import get_sentences
from .normalize import normalize


def fast_tokenize(
    text: Union[List[str], str], ignore_partial: bool = False
) -> List[List[str]]:
    if isinstance(text, str):
        text = normalize(text)
        text = get_sentences(text, ignore_partial=ignore_partial)

    results: List[List[str]] = []

    for sentence in text:
        sentence = re.sub(r"\bare\b", "is", sentence)
        sentence = re.sub(r"\ban\b", "a", sentence)
        sentence = re.sub(r"\bthese\b", "this", sentence)
        results.append(
            [
                token.lower() if token not in {"CITATION", "NUMBER"} else token
                for token in word_tokenizer(sentence)
            ]
        )

    return results
