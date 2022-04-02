from typing import Any, Callable, Optional

from ..core import Plugin
from .load_model import load_model


class UseModelPlugin(Plugin):
    def __init__(
        self,
        function: Callable[[Any], Any],
        key: str,
        version: Optional[int],
        return_path: bool,
    ):
        def wrapper(*args, **kwargs):
            return function(*args, **kwargs, model=self._model)

        super().__init__(wrapper)

        self._key = key
        self._version = version
        self._return_path = return_path

    def on_initialize(self) -> None:
        super().on_initialize()
        self._model = load_model(
            key=self._key, version=self._version, return_path=self._return_path
        )
