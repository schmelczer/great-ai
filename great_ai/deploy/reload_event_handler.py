from threading import RLock, Timer
from typing import Callable, Optional

from watchdog.events import FileSystemEvent, PatternMatchingEventHandler


class ReloadEventHandler(PatternMatchingEventHandler):
    """Debounce edit and replacement events emitted by supported OS observers."""

    def __init__(
        self, restart: Callable[[], None], debounce_seconds: float = 0.3
    ) -> None:
        super().__init__(patterns=["*.py", "*.ipynb"], ignore_patterns=["__*.py"])
        self._restart = restart
        self._debounce_seconds = debounce_seconds
        self._lock = RLock()
        self._timer: Optional[Timer] = None
        self._closed = False

    def on_any_event(self, event: FileSystemEvent) -> None:
        if event.is_directory or event.event_type not in {
            "created",
            "modified",
            "moved",
            "closed",
        }:
            return
        with self._lock:
            if self._closed:
                return
            if self._timer is not None:
                self._timer.cancel()
            self._timer = Timer(self._debounce_seconds, self._run_restart)
            self._timer.daemon = True
            self._timer.start()

    def _run_restart(self) -> None:
        with self._lock:
            if not self._closed:
                self._restart()

    def close(self) -> None:
        with self._lock:
            self._closed = True
            if self._timer is not None:
                self._timer.cancel()
