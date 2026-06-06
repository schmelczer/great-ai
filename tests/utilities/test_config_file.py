import os
from pathlib import Path

import pytest
from great_ai.utilities import ConfigFile

DATA_PATH = Path(__file__).parent.resolve() / "data"


def test_simple() -> None:
    c = ConfigFile(DATA_PATH / "good.conf")
    assert c.zeroth_key == "test"
    assert c.my_hashtag == "#great_ai"
    assert c.first_key == "András"
    assert c.second_key == "test 2"
    assert c.third_key == "test= 2=="
    assert (
        c.fourth_key
        == """
this#
is
multiline
"""
    )
    assert c.whitespace == "hardly  matters"
    with pytest.raises(KeyError):
        c.this


def test_simple_dict() -> None:
    c = ConfigFile(DATA_PATH / "good.conf")
    assert c["zeroth_key"] == "test"
    assert c["first_key"] == "András"
    assert c["my_hashtag"] == "#great_ai"
    assert c["second_key"] == "test 2"
    assert c["third_key"] == "test= 2=="
    assert (
        c["fourth_key"]
        == """
this#
is
multiline
"""
    )
    assert c["whitespace"] == "hardly  matters"
    with pytest.raises(KeyError):
        c["#this"]


def test_string_path() -> None:
    c = ConfigFile(str(DATA_PATH / "good.conf"))
    assert c.zeroth_key == "test"
    assert c.first_key == "András"
    assert c.my_hashtag == "#great_ai"

    assert c.second_key == "test 2"
    assert c.third_key == "test= 2=="
    assert (
        c.fourth_key
        == """
this#
is
multiline
"""
    )
    assert c.whitespace == "hardly  matters"


def test_env() -> None:
    os.environ["alma"] = "12"
    c = ConfigFile(DATA_PATH / "env.conf")
    del os.environ["alma"]
    assert c.first_key == "test"
    assert c.second_key == "12"


def test_env_not_exists() -> None:
    with pytest.raises(ValueError):
        ConfigFile(DATA_PATH / "env-bad.conf")


def test_env_not_exists_fallback() -> None:
    os.environ["alma"] = "12"
    c = ConfigFile(DATA_PATH / "env.conf")
    assert c.fourth_key == "this is a default value"


def test_env_exists_ignore_fallback() -> None:
    os.environ["alma"] = "12"
    os.environ["SOMETHING"] = "hi"
    c = ConfigFile(DATA_PATH / "env.conf")
    del os.environ["SOMETHING"]

    assert c.fourth_key == "hi"


def test_duplicate_key() -> None:
    with pytest.raises(KeyError):
        ConfigFile(DATA_PATH / "bad.conf")
