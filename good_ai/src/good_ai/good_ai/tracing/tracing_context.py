import logging
import threading
from collections import defaultdict
from datetime import datetime
from types import TracebackType
from typing import Any, DefaultDict, List, Optional, Type

from ..views import Model, Trace
from .persistence import PersistenceDriver

logger = logging.getLogger("good_ai")


class TracingContext:
    persistence_driver: PersistenceDriver
    _contexts: DefaultDict[int, List["TracingContext"]] = defaultdict(lambda: [])

    def __init__(self) -> None:
        self._models: List[Model] = []
        self._input: Any = None
        self._output: Any = None
        self._trace: Optional[Trace] = None
        self._start_time = datetime.utcnow()

    def log_input(self, input: Any) -> None:
        self._input = input

    def log_model(self, model: Model) -> None:
        self._models.append(model)

    def log_output(self, output: Any) -> Trace:
        self._output = output

        delta_time = (datetime.utcnow() - self._start_time).microseconds / 1000
        self._trace = Trace(
            created=self._start_time.isoformat(),
            execution_time_ms=delta_time,
            input=self._input,
            models=self._models,
            output=self._output,
        )
        return self._trace

    @classmethod
    def get_current_context(cls) -> Optional["TracingContext"]:
        if cls._contexts[threading.get_ident()]:
            return cls._contexts[threading.get_ident()][-1]
        return None

    def __enter__(self) -> "TracingContext":
        self._contexts[threading.get_ident()].append(self)
        return self

    def __exit__(
        self,
        type: Optional[Type[BaseException]],
        exception: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> bool:
        assert self._contexts[threading.get_ident()][-1] == self
        self._contexts[threading.get_ident()].remove(self)

        if type is None:
            assert self._trace is not None
            self.persistence_driver.save_document(self._trace.dict())
        else:
            logger.exception(f"Could not finish operation: {exception}")

        return True
