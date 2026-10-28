# Installation guide

With [uv](https://docs.astral.sh/uv/getting-started/installation/){ target=_blank } installed, create and activate a Python environment, then install GreatAI:

```sh
uv venv --python 3.13
source .venv/bin/activate
uv pip install great-ai
```
> Python 3.12 or later is required. Python 3.13 is supported.

This will work on all major operating systems.

## Google Colab

To use GreatAI in [Google Colab](https://colab.research.google.com){ target=_blank }, select a runtime with Python 3.12 or later, then run this notebook cell to install uv and GreatAI into the runtime's Python environment:

```python
import sys

!curl -LsSf https://astral.sh/uv/install.sh | sh
!~/.local/bin/uv pip install --system --python {sys.executable} --upgrade great-ai
```

## Command-line tools

After installation, `great-ai` and `large-file` are available as commands. The former is required for deploying your application, while the latter lets you manage models and datasets from your terminal.

??? note "Snakes & kebabs"
    The library is called `great-ai`; therefore, its command-line entry point is also called `great-ai`. However, Python module names cannot contain hyphens, that's why you have to `import great_ai` with an underscore. The `great-ai` CLI tool is also available as `python3 -m great_ai`.

    To help with the confusion, a CLI executable called `great_ai` (and `large_file`) are also installed. Thus, if you prefer, you can always refer to GreatAI using its underscored name variant (`great_ai`).

!!! note "Windows"
    Activate the environment with `.venv\Scripts\activate` in Command Prompt or `.\.venv\Scripts\Activate.ps1` in PowerShell instead of `source .venv/bin/activate`.

    If `great-ai` or `large-file` is unavailable, check that the environment is active, or use `python -m great_ai` and `python -m great_ai.large_file` instead.

## Update

With your virtual environment active, update to the latest version:

```sh
uv pip install --upgrade great-ai
```

## Bleeding edge

You can also install the latest (usually unreleased) version from GitHub.

```sh
uv pip install --upgrade git+https://github.com/schmelczer/great-ai.git
```
> Python 3.12 or later is required.
