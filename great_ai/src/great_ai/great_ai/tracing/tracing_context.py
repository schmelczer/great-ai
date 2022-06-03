import threading
from collections import defaultdict
from datetime import datetime
from types import TracebackType
from typing import Any, DefaultDict, Dict, List, Literal, Optional, Type

from ..context.get_context import get_context
from ..views import Model, Trace


class TracingContext:
    _contexts: DefaultDict[int, List["TracingContext"]] = defaultdict(lambda: [])

    def __init__(self) -> None:
        self._models: List[Model] = []
        self._values: Dict[str, Any] = {}
        self._trace: Optional[Trace] = None
        self._start_time = datetime.utcnow()

    def log_value(self, name: str, value: Any) -> None:
        self._values[name] = value

    def log_model(self, model: Model) -> None:
        self._models.append(model)

    def finalise(self, output: Any = None, exception: BaseException = None) -> Trace:
        assert self._trace is None, "has been already finalised"

        delta_time = (datetime.utcnow() - self._start_time).microseconds / 1000
        self._trace = Trace(
            created=self._start_time.isoformat(),
            execution_time_ms=delta_time,
            logged_values=self._values,
            models=self._models,
            output=output,
            exception=None
            if exception is None
            else f"{type(exception).__name__}: {exception}",
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
    ) -> Literal[False]:
        assert self._contexts[threading.get_ident()][-1] == self
        self._contexts[threading.get_ident()].remove(self)

        if exception is not None and type is not None:
            self.finalise(exception=exception)
            if get_context().should_log_exception_stack:
                get_context().logger.exception("Could not finish operation")
            else:
                get_context().logger.error(
                    f"Could not finish operation because of {type.__name__}: {exception}"
                )

        assert self._trace is not None
        get_context().tracing_database.save(self._trace)

        return False
