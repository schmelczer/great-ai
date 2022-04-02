from typing import Any, Callable


class Plugin:
    def __init__(self, function: Callable[[Any], Any]):
        self._function = function
        self._initialized = False

    def initialize(self):
        if not self._initialized:
            self.on_initialize()
            self._initialized = True

    def on_initialize(self):
        pass

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        assert self._initialized
        return self._function(*args, **kwargs)
