import html
import re
import unicodedata

import unidecode

from .data import left_regular_punctuations, right_regular_punctuations
from .external.pylatexenc.latex2text import LatexNodes2Text
from .logger.get_logger import get_logger

logger = get_logger("clean")
latex = LatexNodes2Text()


joined_left_punctuations = "".join(left_regular_punctuations).replace("]", r"\]")
joined_right_punctuations = "".join(right_regular_punctuations).replace("[", r"\[")


def clean(
    text: str,
    ignore_xml: bool = False,
    ignore_latex: bool = False,
    remove_brackets: bool = False,
    convert_to_ascii: bool = False,
) -> str:
    """Clean all XML, LaTeX, PDF-extraction, and Unicode artifacts from the text.

    The cleaning is quite heavy-weight and can be destructive. However, when working
    with text, this is usually required to achieve sufficient cleanliness before further
    processing.

    Optionally, the text can be turned into ASCII. Carefully consider whether this is
    absolutely needed for your use-case.

    Examples:
        >>> clean('<h2 color="red">Bj\\\\"{o}rn is \\t \\\\textit{happy} 🙂 &lt;3</h2>')
        'Björn is happy 🙂 <3'

        >>> clean(
        ...    '<h2 color="red">Bj\\\\"{o}rn    is \\t \\\\textit{happy} 🙂 &lt;3</h2>',
        ...    convert_to_ascii=True
        ... )
        'Bjorn is happy <3'

        >>> clean(
        ... '<h2 color="red">Bj\\\\"{o}rn       is \\t \\\\textit{happy} 🙂 &lt;3</h2>',
        ... ignore_xml=True
        ... )
        '<h2 color="red">Björn is happy 🙂 lt;3</h2>'

    Args:
        text: Text to be cleaned.
        ignore_xml: Do not process/remove XML-tags.
        ignore_latex: Do not process/remove LaTeX-tags.
        remove_brackets: Do not remove brackets ([])
        convert_to_ascii: Strip (or convert) non-ascii characters.

    Returns:
        The cleaned input text with sensibly collapsed whitespace and optionally no
            markup.
    """

    if not ignore_xml:
        text = re.sub(r"<[^>]*>", " ", text)
        text = html.unescape(text)

    if not ignore_latex:
        text = text.replace("%", "\\%")  # escape LaTeX comments before parsing as LaTeX

        try:
            text = latex.latex_to_text(text, tolerant_parsing=True, strict_braces=False)
            text = text.replace("%s", " ")
        except:
            logger.exception("Latex parsing error")

    if convert_to_ascii:
        text = unicodedata.normalize("NFKD", text)

        try:
            text.encode("ASCII", errors="strict")
        except UnicodeEncodeError:
            text = "".join([c for c in text if not unicodedata.combining(c)])
            text = unidecode.unidecode(text)

    text = re.sub(
        r"\b[a-zA-Z](?:[\t ]+[a-zA-Z]\b)+", lambda m: re.sub(r"[\t ]", "", m[0]), text
    )  # A R T I C L E => ARTICLE

    if remove_brackets:
        text = re.sub(r"\[[^\]]*\]", " ", text)

    # fix hypens: break- word => break-word
    text = re.sub(r"(\S)-\s+", r"\1-", text)
    text = re.sub(r"\s+-(\S)", r"-\1", text)

    # collapse whitespace
    text = re.sub(r"\s+", " ", text)

    # fix punctuation
    text = re.sub(rf" ([{joined_left_punctuations}])", r"\1", text)
    text = re.sub(rf"([{joined_right_punctuations}]) ", r"\1", text)

    text = text.strip()

    return text
