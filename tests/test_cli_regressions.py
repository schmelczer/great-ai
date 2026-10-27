from threading import Event

from watchdog.events import FileClosedEvent, FileModifiedEvent, FileMovedEvent

from great_ai.deploy.reload_event_handler import ReloadEventHandler


def test_reload_debounces_edit_and_replacement_events() -> None:
    completed = Event()
    calls = []

    def restart() -> None:
        calls.append("restart")
        completed.set()

    handler = ReloadEventHandler(restart, debounce_seconds=0.02)
    try:
        handler.dispatch(FileModifiedEvent("service.py"))
        handler.dispatch(FileClosedEvent("service.py"))
        handler.dispatch(FileMovedEvent("temporary", "service.py"))
        assert completed.wait(timeout=2)
        assert calls == ["restart"]
        handler.dispatch(FileModifiedEvent("__service__.py"))
    finally:
        handler.close()
    handler.dispatch(FileModifiedEvent("service.py"))
    assert calls == ["restart"]
