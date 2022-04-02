from typing import Optional

from langcodes import Language
from langdetect import LangDetectException, detect


def predict_language(text: Optional[str]) -> str:
    if not text:
        return Language.make().to_tag()

    try:
        language_code = detect(text)
    except LangDetectException:
        return Language.make().to_tag()

    return Language.get(language_code).to_tag()
