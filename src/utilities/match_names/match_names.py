import functools
import re
from typing import List, Optional, Tuple

from ..clean import clean
from .config import (
    first_name_weight,
    infixes_weight,
    initials_weight,
    last_name_weight,
    match_threshold,
)
from .name_parts import NameParts


def match_names(n1: Optional[str], n2: Optional[str]) -> bool:
    score = get_name_match_score(n1, n2)
    return score > match_threshold


def get_name_match_score(n1: Optional[str], n2: Optional[str]) -> float:
    if not n1 or not n2:
        return 0

    p1 = get_name_parts(n1)
    p2 = get_name_parts(n2)

    for f1 in p1.first_names:
        for f2 in p2.first_names:
            if f1[0] == f2[0]:
                p1.initials = [i for i in p1.initials if i != f1[0]]
                p2.initials = [i for i in p2.initials if i != f1[0]]

    last_name_score = last_name_weight * _match_percentage(p1.last_names, p2.last_names)
    first_name_score = first_name_weight * _match_percentage(
        p1.first_names, p2.first_names
    )
    initials_score = initials_weight * _match_percentage(p1.initials, p2.initials)
    infixes_score = min(0, infixes_weight * _match_percentage(p1.infixes, p2.infixes))

    return last_name_score + first_name_score + initials_score + infixes_score


def get_name_parts(name: str) -> NameParts:
    result = _get_name_parts(name)
    return result.copy()


@functools.lru_cache(maxsize=None)
def _get_name_parts(name: str) -> NameParts:
    name = _clean_name(name)

    first_names, name = _get_parenthesized_first_names(name)
    initials, name = _get_initials(name)

    last_names = []
    infixes, name = _get_infixes(name)
    if "," in name:
        [last_name, *rest] = name.split(",")
        rest_combined = " ".join(rest)
        last_names.extend(last_name.split(" "))
        first_names.extend(rest_combined.split(" "))
    else:
        parts = name.strip().split(" ")
        if parts:
            last_names.append(parts[-1])
            parts.pop(-1)
            first_names.extend(parts)
        else:
            last_names.append(name)

    first_names = [f for f in first_names if f]
    for f in first_names:
        if all(f[0] != i for i in initials):
            initials.append(f[0])

    return NameParts(
        first_names=first_names,
        initials=initials,
        infixes=infixes,
        last_names=[
            name
            for last_name in last_names
            for name in (last_name.split("-") if "-" in last_name else [last_name])
            if name
        ],
    )


def _clean_name(name: str) -> str:
    name = clean(name, convert_to_ascii=True)

    name = re.sub(
        r"""
            (MD|PhD|Ir|dr|Dr|DR|MSc|MA|BSc|BA|Prof)
            [,.]?
            [ ]*
        """,
        "",
        name,
        flags=re.VERBOSE,
    )

    subs_made = 1
    while subs_made:
        name, subs_made = re.subn(r"([A-Z]\.)\s+([A-Z])\b", r"\g<1>\g<2>", name)

    name = name.replace(r"\s+-\s+", "-")
    name = " ".join(p for p in name.split(" ") if p)
    name = re.sub(r"^([^,.]+) ([A-Z])$", r"\g<1>, \g<2>.", name)
    return name


def _get_parenthesized_first_names(name: str) -> Tuple[List[str], str]:
    groups = re.search(r"\(([a-zA-Z ]+)\)", name)
    if groups:
        return (
            groups.group(1).split(" "),
            _remove_between_indices(name, groups.start(), groups.end()),
        )

    return [], name


def _get_initials(n: str) -> Tuple[List[str], str]:
    initials = []

    groups = re.search(r"\b(?P<abr1>([A-Z]\.)*)(?P<abr2>[A-Z])(\.|$)", n)
    if groups:
        first_name_abbreviations = [
            *groups.group("abr1").split("."),
            groups.group("abr2"),
        ]
        first_name_abbreviations = [f for f in first_name_abbreviations if f != ""]
        initials.extend(first_name_abbreviations)
        n = _remove_between_indices(n, groups.start(), groups.end())

    return initials, n


def _get_infixes(n: str) -> Tuple[List[str], str]:
    infixes = ["de", "van", "der", "den", "te", "ter", "ten"]

    parts = n.split(" ")
    return [p for p in parts if p.lower() in infixes], " ".join(
        p for p in parts if p.lower() not in infixes
    )


def _remove_between_indices(s: str, start: int, end: int) -> str:
    return s[:start] + s[end:]


def _match_percentage(l1: List[str], l2: List[str]) -> float:
    if not l1 or not l2:
        return 0

    s1 = set(l1)
    s2 = set(l2)
    common_q = 2 * len(s1 & s2) / (len(s1) + len(s2))
    different_q = min(len(s1 - s2) / len(s1), len(s2 - s1) / len(s2))
    return common_q - different_q
