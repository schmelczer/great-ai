from pathlib import Path
from typing import Dict, List, Union

import yaml
from spacy.matcher import Matcher

from ..get_sentences import get_sentences
from ..nlp import nlp
from .fast_tokenize import fast_tokenize
from .normalize import normalize

rules_cache: Dict[str, Matcher] = {}


def filter_sentences(
    sentences: str,
    rules_file: Path,
    inverse: bool = False,
    ignore_partial: bool = False,
) -> List[str]:
    if str(rules_file) not in rules_cache:
        with open(rules_file, encoding="utf-8") as f:
            rule_patterns = yaml.safe_load(f).keys()

        matcher = Matcher(nlp.vocab)
        rules = [_pattern_to_rule(p) for p in rule_patterns]
        matcher.add("", rules)
        rules_cache[str(rules_file)] = matcher

    matcher = rules_cache[str(rules_file)]

    original_sentences = get_sentences(sentences, ignore_partial=ignore_partial)

    tokenized = fast_tokenize(original_sentences, ignore_partial=ignore_partial)

    results: List[str] = []
    for original_sentence, sentence in zip(original_sentences, tokenized):
        doc = nlp(normalize(" ".join(sentence)))
        matches = matcher(doc)
        if matches:
            # _, start, end = max(
            #     matches,
            #     key=lambda v: v[2] - v[1],
            # )
            # print(str(doc[start:end]))

            if not inverse:
                results.append(original_sentence)
        elif inverse:
            results.append(original_sentence)

    return results


def _pattern_to_rule(pattern: str) -> List[Dict[str, Union[bool, str]]]:
    result: List[Dict[str, Union[bool, str]]] = []
    for t in pattern.split():
        if t == "*":
            result.extend([{"OP": "?"}, {"OP": "?"}])
        elif t == "CITATION":
            result.append({"ORTH": "CITATION"})
        elif t == "NUMBER":
            result.append({"ORTH": "NUMBER"})
        else:
            result.append({"LOWER": t})
    return result
