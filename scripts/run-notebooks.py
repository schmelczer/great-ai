#!/usr/bin/env python3
"""Execute documentation notebooks in order, with the current Python interpreter."""

import argparse
import os
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

import nbformat
from jupyter_client import KernelManager
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = [
    "docs/tutorial/train.ipynb",
    "docs/tutorial/deploy.ipynb",
    "docs/examples/simple/data.ipynb",
    "docs/examples/simple/train.ipynb",
    "docs/examples/simple/deploy.ipynb",
    "docs/examples/simple/stacked-bars.ipynb",
    "docs/examples/simple-mag/train.ipynb",
    "docs/examples/scibert/data.ipynb",
    "docs/examples/scibert/train.ipynb",
    "docs/examples/scibert/deploy.ipynb",
    "docs/surveys/surveys.ipynb",
]

CHECK_DEPLOYMENT = """
import sys
from importlib import import_module
from pathlib import Path

from fastapi.testclient import TestClient
from great_ai.__main__ import find_app, get_script_name, get_script_name_of_notebook

notebook = sys.argv[1]
try:
    module_name = get_script_name(notebook)
    app_name = find_app(module_name)
    assert app_name is not None, "The CLI could not import the deployment notebook"
    module = import_module(module_name)
    function_name = app_name.split(":")[1].split(".")[0]
    service = getattr(module, function_name)
    argument = "text" if sys.argv[2] == "simple" else "sentence"
    with TestClient(service.app) as client:
        response = client.post("/predict", json={argument: "Neural networks learn useful features."})
        response.raise_for_status()
        assert response.json()["output"] is not None
finally:
    Path(get_script_name_of_notebook(notebook)).unlink(missing_ok=True)
"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("notebooks", nargs="*", help="Paths relative to the repository")
    parser.add_argument("--timeout", type=int, default=600, help="Seconds per cell")
    args = parser.parse_args()
    output_dir = (
        ROOT
        / ".cache/executed-notebooks"
        / f"python{sys.version_info.major}.{sys.version_info.minor}"
    )
    output_dir.mkdir(parents=True, exist_ok=True)

    # A fresh workspace detects missing dependencies between notebook stages and
    # avoids silently passing because an old model or database happens to exist.
    with TemporaryDirectory(prefix="great-ai-notebooks-") as workspace:
        env = dict(os.environ)
        env["PYTHONPATH"] = os.pathsep.join(
            filter(None, [str(ROOT), env.get("PYTHONPATH")])
        )
        for name in args.notebooks or NOTEBOOKS:
            path = (ROOT / name).resolve()
            relative = path.relative_to(ROOT)
            # Related notebooks share the library's default local storage.
            work_dir = Path(workspace) / relative.parent
            work_dir.mkdir(parents=True, exist_ok=True)
            print(f"Running {relative}", flush=True)
            notebook = nbformat.read(path, as_version=4)
            nbformat.validate(notebook)
            manager = KernelManager(kernel_name="python3")
            # Do not depend on a user-installed kernelspec pointing at this venv.
            manager.kernel_spec.argv = [
                sys.executable,
                "-m",
                "ipykernel_launcher",
                "-f",
                "{connection_file}",
            ]
            client = NotebookClient(notebook, km=manager, timeout=args.timeout)
            try:
                client.execute(cwd=str(work_dir), env=env, cleanup_kc=True)
            finally:
                destination = output_dir / relative
                destination.parent.mkdir(parents=True, exist_ok=True)
                nbformat.write(notebook, destination)
            if path.stem == "deploy":
                subprocess.run(
                    [
                        sys.executable,
                        "-c",
                        CHECK_DEPLOYMENT,
                        str(destination),
                        path.parent.name,
                    ],
                    cwd=work_dir,
                    env=env,
                    check=True,
                    timeout=args.timeout,
                    stdout=subprocess.DEVNULL,
                )
            print(f"Passed {relative}", flush=True)
    print(f"Executed notebooks saved to {output_dir}", flush=True)


if __name__ == "__main__":
    main()
