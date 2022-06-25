from pathlib import Path
import os
from typing import Dict, Union

from ..logger import get_logger
from .parse_error import ParseError
from .pattern import pattern

ENVIRONMENT_VARIABLE_KEY_PREFIX = 'ENV'

logger = get_logger('ConfigFile')

class ConfigFile:
    def __init__(self, path: Union[Path, str], ignore_missing_environment_variables:bool=False) -> None:
        if not isinstance(path, Path):
            path = Path(path)
        self._path = path
        self._ignore_missing_environment_variables = ignore_missing_environment_variables
        self._key_values: Dict[str, str] = {}

        self._parse()

    def _parse(self):
        with open(self._path, encoding='utf-8') as f:
            lines: str = f.read()

        matches = pattern.findall(lines)
        for key, *values in matches:
            if key in self._key_values:
                raise KeyError(f'Key `{key}` has been already defined and its value is `{value}`')

            try:
                value = next(v for v in values if v)
            except StopIteration:
                raise ParseError(f'Cannot parse config file ({self._path.absolute()}), error at key `{key}`')

            if value.startswith(f'{ENVIRONMENT_VARIABLE_KEY_PREFIX}:'):
                _, value = value.split(':')
                if value not in os.environ:
                    issue = f'The value of `{key}` contains the "{ENVIRONMENT_VARIABLE_KEY_PREFIX}` prefix but `{value}` is not defined as an environment variable'
                    if self._ignore_missing_environment_variables:
                        logger.warning(f'{issue}, defaulting to `None`')
                    else:
                        raise KeyError(issue)
                value = os.environ[value]
            
            self._key_values[key] = value

    def __getattr__(self, key: str) -> str:
        if key in self._key_values:
            return self._key_values[key]
        raise KeyError(f'Key `{key}` is not found in configuration file ({self._path.absolute()})')
