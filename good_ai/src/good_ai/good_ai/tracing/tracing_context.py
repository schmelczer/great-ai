import threading
from collections import defaultdict
from datetime import datetime
from types import TracebackType
from typing import Any, DefaultDict, Dict, List, Optional, Type

from ..context import get_context
from ..views import Model, Trace


class TracingContext:
    _contexts: DefaultDict[int, List["TracingContext"]] = defaultdict(lambda: [])

    def __init__(self) -> None:
        self._models: List[Model] = []
        self._values: Dict[str, Any] = {}
        self._output: Any = None
        self._trace: Optional[Trace] = None
        self._start_time = datetime.utcnow()

    def log_value(self, name: str, value: Any) -> None:
        self._values[name] = value

    def log_model(self, model: Model) -> None:
        self._models.append(model)

    def log_output(self, output: Any, evaluation_id: Optional[str] = None) -> Trace:
        self._output = output

        delta_time = (datetime.utcnow() - self._start_time).microseconds / 1000
        self._trace = Trace(
            evaluation_id=evaluation_id,
            created=self._start_time.isoformat(),
            execution_time_ms=delta_time,
            logged_values=self._values,
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
            get_context().persistence.save_document(self._trace)
        else:
            get_context().logger.exception(f"Could not finish operation: {exception}")

        return True
