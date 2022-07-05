from great_ai.large_file.helper import human_readable_to_byte


def test_simple_cases() -> None:
    assert human_readable_to_byte("1KB") == 1024
    assert human_readable_to_byte("2KB") == 2048


def test_fractions() -> None:
    assert human_readable_to_byte("0.5KB") == 512
    assert human_readable_to_byte("20.5KB") == 1024 * 20 + 512


def test_formatting() -> None:
    assert human_readable_to_byte(" 1MB") == 1024 * 1024
    assert human_readable_to_byte(" 2  MB") == 1024 * 1024 * 2
    assert human_readable_to_byte("    4   MB ") == 1024 * 1024 * 4
    assert human_readable_to_byte("8MB    ") == 1024 * 1024 * 8
    assert human_readable_to_byte(" 1.5   MB  ") == 1024 * 1024 * 1.5


def test_casing() -> None:
    assert human_readable_to_byte("0.5GB") == 0.5 * 1024 * 1024 * 1024
    assert human_readable_to_byte("0.5gB") == 0.5 * 1024 * 1024 * 1024
    assert human_readable_to_byte("0.5Gb") == 0.5 * 1024 * 1024 * 1024
    assert human_readable_to_byte("0.5gb") == 0.5 * 1024 * 1024 * 1024
