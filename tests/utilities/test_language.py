from great_ai.utilities import english_name_of_language, is_english, predict_language


def test_predict_language() -> None:
    assert predict_language("This is an English text.") == "en"
    assert predict_language("Ez egy magyar szöveg.") == "hu"
    assert predict_language("32") == "und"
    assert predict_language("") == "und"


def test_is_english() -> None:
    assert is_english("en")
    assert is_english("en-US")
    assert not is_english("hu")
    assert not is_english("de")
    assert not is_english("zh")
    assert not is_english("zh-TW")
    assert not is_english("und")
    assert not is_english("")
    assert not is_english(None)


def test_english_name_of_language() -> None:
    assert english_name_of_language("en") == "English"
    assert english_name_of_language("hu") == "Hungarian"
    assert english_name_of_language("zh") == "Chinese"
    assert english_name_of_language("zh-TW") == "Chinese (Taiwan)"
    assert english_name_of_language("und") == "Unknown language"
    assert english_name_of_language("") == "Unknown language"
    assert english_name_of_language(None) == "Unknown language"
