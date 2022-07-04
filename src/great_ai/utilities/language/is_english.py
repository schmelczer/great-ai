from typing import Optional

from langcodes import standardize_tag, tag_distance


def is_english(language_code: Optional[str]) -> bool:
    if not language_code:
        language_code = "und"

    language_code = standardize_tag(language_code)
    return tag_distance(language_code, "en") < 15
