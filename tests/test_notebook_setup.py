import json
from pathlib import Path
from typing import Any, Dict

import pytest
from great_ai import ParallelTinyDbDriver
from great_ai.context import get_context
from great_ai.large_file import LargeFileLocal

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = sorted((ROOT / "docs").rglob("*.ipynb"))


@pytest.mark.parametrize(
    "notebook", NOTEBOOKS, ids=lambda path: str(path.relative_to(ROOT))
)
def test_notebook_setup_uses_checkout_paths_from_another_directory(
    isolated_context: None,
    notebook: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.syspath_prepend(str(ROOT))
    from docs import notebook_support

    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("GREAT_AI_NOTEBOOK_WORKDIR", str(tmp_path))
    monkeypatch.setattr(notebook_support, "FULL_RUN", False)
    monkeypatch.setattr(ParallelTinyDbDriver, "path_to_db", tmp_path / "traces.json")
    cells = json.loads(notebook.read_text())["cells"]
    setup = next(
        "".join(cell["source"]) for cell in cells if cell["cell_type"] == "code"
    )
    namespace: Dict[str, Any] = {}
    exec(compile(setup, str(notebook), "exec"), namespace)
    work_dir = tmp_path / notebook.parent.name
    assert work_dir.is_dir()
    assert LargeFileLocal.cache_path == work_dir / "models-cache"
    database = get_context().tracing_database
    assert isinstance(database, ParallelTinyDbDriver)
    assert database.path_to_db == work_dir / "tracing_database.json"
    assert (notebook_support.DATA_DIR / "train.txt").is_file()
