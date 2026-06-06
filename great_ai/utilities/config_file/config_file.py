import os
from pathlib import Path
from typing import Dict, ItemsView, Iterator, KeysView, Mapping, Union, ValuesView

from ..logger.get_logger import get_logger
from .parse_error import ParseError
from .pattern import pattern

logger = get_logger("ConfigFile")


class ConfigFile(Mapping[str, str]):
    """A small and safe `INI`-style configuration loader with `dict` and `ENV` support.

    The values can be accessed using both dot- and index-notation. It is compatible
    with the `dict` interface.

    File format example:

    ```toml
    # comments are allowed everywhere

    key = value  # you can leave or omit whitespace around the equal-sign
    my_hashtag = "#great_ai" # the r-value can be quoted with " or ' or `.

    my_var = my_default_value  # Default values can be given to env-vars,
                               # see next line. The default value must come first.

    my_var = ENV:MY_ENV_VAR    # If the value starts with the `ENV:` prefix,
                               # it is looked up from the environment variables.
    ```

    Examples:
        >>> ConfigFile('tests/utilities/data/simple.conf')
        ConfigFile(path=tests/utilities/data/simple.conf) {'zeroth_key': 'test', 'first_key': 'András'}

        >>> ConfigFile('tests/utilities/data/simple.conf').zeroth_key
        'test'

        >>> ConfigFile('tests/utilities/data/simple.conf').second_key
        Traceback (most recent call last):
        ...
        KeyError: 'Key `second_key` is not found in configuration file ...

        >>> a = ConfigFile('tests/utilities/data/simple.conf')
        >>> {**a}
        {'zeroth_key': 'test', 'first_key': 'András'}

    """

    ENVIRONMENT_VARIABLE_KEY_PREFIX = "ENV"

    def __init__(self, path: Union[Path, str], *, ignore_missing: bool = False) -> None:
        """Load and parse a configuration file.

        Everything is eager-loaded, thus, exceptions may be thrown here.

        Args:
            path: Local path of the configuration file.
            ignore_missing: Don't raise an exception on missing environment variables.

        Raises:
            FileNotFoundError: If there is no file at the specified path.
            ParseError: If the provided file does not conform to the expected format.
            KeyError: If there is duplication in the keys.
            ValueError: If an environment variable is referenced but it is not set in
                the system and `ignore_missing=False`.
        """

        if not isinstance(path, Path):
            path = Path(path)

        if not path.exists():
            raise FileNotFoundError(path.absolute())

        self._ignore_missing = ignore_missing

        self._path = path
        self._key_values: Dict[str, str] = {}

        self._parse()

    @property
    def path(self) -> Path:
        """Original path from where the configuration was loaded."""
        return self._path

    def _parse(self) -> None:
        with open(self._path, encoding="utf-8") as f:
            lines: str = f.read()

        matches = pattern.findall(lines)
        for key, *values in matches:
            try:
                value = next(v for v in values if v)
            except StopIteration:
                raise ParseError(
                    f"""Cannot parse config file ({
                        self._path.absolute()
                        }), error at key `{key}`"""
                )

            already_exists = key in self._key_values
            if already_exists and not value.startswith(
                f"{self.ENVIRONMENT_VARIABLE_KEY_PREFIX}:"
            ):
                raise KeyError(
                    f"Key `{key}` has been already defined and its value is `{self._key_values[key]}`"
                )

            if value.startswith(f"{self.ENVIRONMENT_VARIABLE_KEY_PREFIX}:"):
                _, value = value.split(":")
                if value not in os.environ:
                    issue = f"""The value of `{key}` contains the "{
                        self.ENVIRONMENT_VARIABLE_KEY_PREFIX
                    }` prefix but `{value}` is not defined as an environment variable"""
                    if already_exists:
                        logger.warning(
                            f"""{issue}, using the default value defined above (`{
                                self._key_values[key]
                            }`)"""
                        )
                        continue
                    elif self._ignore_missing:
                        logger.warning(issue)
                    else:
                        raise ValueError(
                            f"{issue} and no default value has been provided"
                        )
                else:
                    value = os.environ[value]

            self._key_values[key] = value

    def __getattr__(self, key: str) -> str:
        if key in self._key_values:
            return self._key_values[key]
        raise KeyError(
            f"Key `{key}` is not found in configuration file ({self._path.absolute()})"
        )

    __getitem__ = __getattr__

    def __iter__(self) -> Iterator[str]:
        return iter(self._key_values)

    def __len__(self) -> int:
        return len(self._key_values)

    def keys(self) -> KeysView[str]:
        return self._key_values.keys()

    def values(self) -> ValuesView[str]:
        return self._key_values.values()

    def items(self) -> ItemsView[str, str]:
        return self._key_values.items()

    def __repr__(self) -> str:
        return f"{type(self).__name__}(path={self._path.as_posix()}) {self._key_values}"
