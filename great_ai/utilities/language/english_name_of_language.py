from typing import Optional

from langcodes import Language


def english_name_of_language(language_code: Optional[str]) -> str:
    """Human-friendly English name of language from its `language_code`.

    A thin wrapper over [langcodes](https://github.com/rspeer/langcodes) for convenient
    language tagging.

    Examples:
        >>> english_name_of_language('en-US')
        'English (United States)'

        >>> english_name_of_language('und')
        'Unknown language'

    Args:
        language_code: Language code, for example, returned by
            [great_ai.utilities.language.predict_language.predict_language][].

    Returns:
        English name of language.
    """

    if not language_code:
        language_code = "und"

    return Language.get(language_code).display_name()
