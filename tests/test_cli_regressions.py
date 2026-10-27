import importlib
from threading import Event
from unittest.mock import patch

import pytest
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


@pytest.mark.parametrize(
    "module_name, operation",
    [
        ("great_ai.__main__", "serve"),
        ("great_ai.large_file.__main__", "handle_command"),
    ],
)
def test_cli_operational_errors_exit_nonzero(module_name: str, operation: str) -> None:
    module = importlib.import_module(module_name)
    with patch.object(module, operation, side_effect=ValueError("failed")):
        with pytest.raises(SystemExit) as error:
            module.main()
    assert error.value.code == 1
