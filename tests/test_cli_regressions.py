import importlib
from pathlib import Path
from threading import Event
from unittest.mock import patch

import pytest
from great_ai.deploy.reload_event_handler import ReloadEventHandler
from watchdog.events import FileClosedEvent, FileModifiedEvent, FileMovedEvent


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


def test_cli_resolves_nested_scripts_and_notebooks(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from great_ai.__main__ import get_script_name, get_script_name_of_notebook

    monkeypatch.syspath_prepend(str(tmp_path))
    package = tmp_path / "nested"
    package.mkdir()
    (package / "__init__.py").write_text("")
    (package / "service.py").write_text("value = 7\n")
    monkeypatch.chdir(tmp_path)
    assert get_script_name("nested/service.py") == "nested.service"
    assert importlib.import_module("nested.service").value == 7
    assert get_script_name(str(package / "service.py")) == "nested.service"
    assert (
        get_script_name_of_notebook("nested/service.ipynb") == "nested/__service__.py"
    )
