import re

from ..clean import clean


def normalize(text: str) -> str:
    text = re.sub(
        r"""
            ([A-Z]\w+\W+(et\ al.))     # inline reference: Bank et al.
            | (\[[0-9-, ]+\])          # IEEE style: [1], [2-4], [3, 5]
            | (\(.*?,?\W+?\d+\))       # APA style: (Bank, 2020)
            | ([A-Z]\w+ \(?\d+\))      # APA style: Bank (2020)
        """,
        " CITATION ",
        text,
        flags=re.VERBOSE,
    )
    text = re.sub(r"\d[\d,. -]*(st|nd|rd|th)?", " NUMBER ", text)
    text = clean(text, convert_to_ascii=True)
    text = re.sub(r"[^a-zA-Z.?!,:;'\" -]", "", text)

    return text
