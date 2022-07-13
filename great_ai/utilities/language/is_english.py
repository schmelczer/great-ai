from typing import Optional

from langcodes import standardize_tag, tag_distance


def is_english(language_code: Optional[str]) -> bool:
    """Decide whether the `language_code` is of an English language.

    A thin wrapper over [langcodes](https://github.com/rspeer/langcodes) for convenient
    language tagging.

    Examples:
        >>> is_english('en-US')
        True

        >>> is_english(None)
        False

        >>> is_english('und')
        False

    Args:
        language_code: Language code, for example, returned by
            `[great_ai.utilities.language.predict_language.predict_language][].

    Returns:
        Boolean indicating whether it's English.
    """
    if not language_code:
        language_code = "und"

    language_code = standardize_tag(language_code)
    return tag_distance(language_code, "en") < 15
