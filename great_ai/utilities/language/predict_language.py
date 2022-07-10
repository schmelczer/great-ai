from typing import Optional

from langcodes import Language
from langdetect import LangDetectException, detect


def predict_language(text: Optional[str]) -> str:
    """Predict the language code from text.

    A thin wrapper over [langcodes](https://github.com/rspeer/langcodes) for convenient
    language tagging.

    Examples:
        >>> predict_language('This is a sentence.')
        'en'

    Args:
        text: Text used for prediction.

    Returns:
        The predicted language code (en, en-US) or `und` if a prediction could not be
            made.
    """

    if not text:
        return Language.make().to_tag()

    try:
        language_code = detect(text)
    except LangDetectException:
        return Language.make().to_tag()

    return Language.get(language_code).to_tag()
