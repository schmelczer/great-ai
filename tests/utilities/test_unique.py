from great_ai.utilities import unique

original = [
    ("a", 1),
    ("b", 5),
    ("a", -3),
    ("c", 5),
    ("d", 2),
    ("a", 2),
]


def test_default() -> None:
    values = [
        *original,
        ("a", 2),
        ("a", 1),
        ("a", -3),
        ("b", 5),
        ("c", 5),
        ("d", 2),
    ]

    expected = original

    assert unique(values) == expected
    assert unique(values, key=lambda v: v) == expected


def test_with_key_0() -> None:
    values = original

    expected = [
        ("a", 1),
        ("b", 5),
        ("c", 5),
        ("d", 2),
    ]

    assert unique(values, key=lambda v: v[0]) == expected


def test_with_key_1() -> None:
    values = original

    expected = [
        ("a", 1),
        ("b", 5),
        ("a", -3),
        ("d", 2),
    ]

    assert unique(values, key=lambda v: v[1]) == expected
