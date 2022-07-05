from great_ai.utilities import get_sentences


def test_default() -> None:
    text = "This is a complete sentence. So is this. However this is n"  # ot.
    expected = ["This is a complete sentence.", "So is this.", "However this is n"]

    assert get_sentences(text) == expected
    assert get_sentences(text, ignore_partial=True) == expected[0:2]


def test_complex() -> None:
    text = """
    This is a complete sentence. So is this.
    End of paragraph.


    Negation contractions (like don't or ain't) are resolved.

    However this is not a sent
    """

    expected = [
        "This is a complete sentence.",
        "So is this.",
        "End of paragraph.",
        "Negation contractions (like don't or ain't) are resolved.",
        "However this is not a sent",
    ]

    print(get_sentences(text, ignore_partial=True))

    assert get_sentences(text) == expected
    assert get_sentences(text, ignore_partial=True) == expected[:-1]


def test_true_casing() -> None:
    text = "This is also referred to as a Convolutional Neural Network (CNN)."
    expected = ["this is also referred to as a Convolutional Neural Network (CNN)."]

    assert get_sentences(text, true_case=True) == expected


def test_remove_punctuation() -> None:
    text = "Also, we --- the authors --- have to find less intrusive, and higher potential procedures. "
    expected = [
        "Also we the authors have to find less intrusive and higher potential procedures"
    ]

    assert get_sentences(text, remove_punctuation=True) == expected


def test_empty() -> None:
    assert get_sentences("") == []
    assert get_sentences(" ") == []
    assert get_sentences("  \n ") == []
    assert get_sentences("", ignore_partial=True) == []
    assert get_sentences("", true_case=True) == []
    assert get_sentences("", remove_punctuation=True) == []
