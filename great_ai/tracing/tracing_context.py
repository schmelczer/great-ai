from contextvars import ContextVar
from datetime import datetime
from time import perf_counter
from types import TracebackType
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, cast
from uuid import uuid4

from typing_extensions import Literal  # <= Python 3.7

from ..constants import DEVELOPMENT_TAG_NAME, ONLINE_TAG_NAME, PRODUCTION_TAG_NAME
from ..context import get_context
from ..views import Model, Trace

T = TypeVar("T")


class TracingContext(Generic[T]):
    """Provide a global context variable throughout the life-cycle of a prediction.

    Should only be used by internal great-ai functions.
    """

    def __init__(self, function_name: str, do_not_persist_traces: bool) -> None:
        self._do_not_persist_traces = do_not_persist_traces
        self._models: List[Model] = []
        self._values: Dict[str, Any] = {}
        self._trace: Optional[Trace[T]] = None
        self._start_datetime = datetime.utcnow()
        self._start_time = perf_counter()
        self._name = function_name

    def log_value(self, name: str, value: Any) -> None:
        self._values[name] = value

    def log_model(self, model: Model) -> None:
        self._models.append(model)

    def finalise(
        self, output: Optional[T] = None, exception: Optional[BaseException] = None
    ) -> Trace[T]:
        assert self._trace is None, "has been already finalised"

        delta_time = round((perf_counter() - self._start_time) * 1000, 4)
        self._trace = (
            cast(  # avoid ValueError: "Trace" object has no field "__orig_class__"
                Trace[T],
                Trace(
                    trace_id=str(uuid4()),
                    created=self._start_datetime.isoformat(),
                    original_execution_time_ms=delta_time,
                    logged_values=self._values,
                    models=self._models,
                    output=output,
                    exception=None
                    if exception is None
                    else f"{type(exception).__name__}: {exception}",
                    tags=[
                        self._name,
                        ONLINE_TAG_NAME,
                        PRODUCTION_TAG_NAME
                        if get_context().is_production
                        else DEVELOPMENT_TAG_NAME,
                    ],
                ),
            )
        )

        return self._trace

    @staticmethod
    def get_current_tracing_context() -> Optional["TracingContext"]:
        return _current_tracing_context.get()

    def __enter__(self) -> "TracingContext":
        _current_tracing_context.set(self)
        return self

    def __exit__(
        self,
        type: Optional[Type[BaseException]],
        exception: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Literal[False]:
        _current_tracing_context.set(None)

        if exception is not None and type is not None:
            self.finalise(exception=exception)
            if get_context().should_log_exception_stack:
                get_context().logger.exception("Could not finish operation")
            else:
                get_context().logger.error(
                    f"Could not finish operation because of {type.__name__}: {exception}"
                )

        assert self._trace is not None
        if not self._do_not_persist_traces:
            get_context().tracing_database.save(self._trace)

        return False


_current_tracing_context: ContextVar[Optional[TracingContext]] = ContextVar(
    "_current_tracing_context", default=None
)
