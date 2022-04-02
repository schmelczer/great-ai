from collections import defaultdict
from typing import Any, Callable, DefaultDict, List

from .plugin import Plugin


class FunctionRegistry:
    def __init__(self) -> None:
        self._registered_functions: DefaultDict[int, List[Plugin]] = defaultdict(
            lambda: []
        )

    def add_plugin(self, function: Callable[..., Any], plugin: Plugin):
        self._registered_functions[id(function)].append(plugin)

    def get_plugins(self, function: Callable[..., Any]) -> List[Plugin]:
        plugins = self._registered_functions[id(function)]
        for p in plugins:
            p.initialize()
        return plugins


function_registry = FunctionRegistry()
