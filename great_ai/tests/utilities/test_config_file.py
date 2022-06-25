import unittest
from pathlib import Path

import pytest

from src.great_ai.utilities import ConfigFile

DATA_PATH = Path(__file__).parent.resolve() / "data"


class TestConfigFile(unittest.TestCase):
    def test_simple(self) -> None:
        c = ConfigFile(DATA_PATH / "good.conf")
        assert c.zeroth_key == "test"
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

    def test_simple_dict(self) -> None:
        c = ConfigFile(DATA_PATH / "good.conf")
        assert c["zeroth_key"] == "test"
        assert c["first_key"] == "András"
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

    def test_string_path(self) -> None:
        c = ConfigFile(str(DATA_PATH / "good.conf"))
        assert c.zeroth_key == "test"
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

    def test_env(self) -> None:
        import os

        os.environ["alma"] = "12"
        c = ConfigFile(DATA_PATH / "env.conf")
        del os.environ["alma"]
        assert c.first_key == "test"
        assert c.second_key == "12"

    def test_env_not_exists(self) -> None:
        with pytest.raises(KeyError):
            ConfigFile(DATA_PATH / "env.conf")

    def test_env_not_exists_but_ignored(self) -> None:
        with pytest.raises(KeyError):
            ConfigFile(
                DATA_PATH / "env.conf", ignore_missing_environment_variables=True
            )

    def test_duplicate_key(self) -> None:
        with pytest.raises(KeyError):
            ConfigFile(DATA_PATH / "bad.conf")
