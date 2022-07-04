from typing import Optional

from langcodes import Language


def english_name_of_language(language_code: Optional[str]) -> str:
    if not language_code:
        language_code = "und"

    return Language.get(language_code).display_name()
