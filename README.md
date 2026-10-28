# <img src="https://raw.githubusercontent.com/schmelczer/great-ai/main/docs/media/logo.png" alt="logo of great-ai" width=60 /> GreatAI

> Prepare your prototype AI code for production deployment.

[![PyPI version](https://badge.fury.io/py/great-ai.svg)](https://badge.fury.io/py/great-ai)
[![Downloads](https://pepy.tech/badge/great-ai/month)](https://pepy.tech/project/great-ai)
[![Docker Pulls](https://img.shields.io/docker/pulls/schmelczera/great-ai)](https://hub.docker.com/repository/docker/schmelczera/great-ai)
[![Check](https://git.schmelczer.dev/andras/great-ai/badges/workflows/test.yml/badge.svg?branch=main)](https://git.schmelczer.dev/andras/great-ai/actions?workflow=test.yml)
[![Sonar line coverage](https://sonar.scoutinscience.com/api/project_badges/measure?project=great-ai&metric=coverage)](https://sonar.scoutinscience.com/dashboard?id=great-ai)
[![Sonar LoC](https://sonar.scoutinscience.com/api/project_badges/measure?project=great-ai&metric=ncloc)](https://sonar.scoutinscience.com/dashboard?id=great-ai)

Applying AI is becoming increasingly more accessible, but many case studies have shown that these applications are often deployed poorly. This may lead to suboptimal performance and to introducing unintended biases. GreatAI helps prepare prototype AI code for deployment with tracing, model versioning, and API scaffolding. These engineering features support oversight; they do not establish a model's accuracy, fairness, or trustworthiness, which require evaluation for the intended use case.

## Example

With [uv](https://docs.astral.sh/uv/getting-started/installation/) installed, create and activate a Python environment:

```sh
uv venv --python 3.13
source .venv/bin/activate
uv pip install great-ai
```

Create a new file called `demo.py`

```python
from great_ai import GreatAI

@GreatAI.create
def greeter(name: str) -> str:
    return f"Hello {name}!"
```

Start it by executing `great-ai demo.py`, and find the dashboard at [http://localhost:6060](http://localhost:6060/dashboard).

![demo screen capture](https://raw.githubusercontent.com/schmelczer/great-ai/main/docs/media/demo.gif)

That's it. Your GreatAI service is _nearly_ ready for production use. Many of the [SE4ML best practices](https://se-ml.github.io) are configured and implemented automatically (of course, these can be customised as well).

Before production, replace the default local TinyDB tracing database with a production-suitable backend, configure storage and deployment infrastructure, and review the remaining best practices for your use case.

> **Published documentation:** [Read the rendered guides, API reference, and notebooks](https://great-ai.schmelczer.dev). The files under `docs/` use MkDocs features that repository previews may not render.

## Why is this GREAT?

![scope of GreatAI](https://raw.githubusercontent.com/schmelczer/great-ai/main/docs/media/scope-simple.drawio.svg)

GreatAI fits between the prototype and deployment phases of your AI development lifecycle. This is highlighted in blue in the diagram. Here, several best practices can be automatically implemented, aiming to achieve the following attributes:

- **G**eneral: use any Python library without restriction
- **R**obust: have error-handling and well-tested utilities out-of-the-box
- **E**nd-to-end: utilise end-to-end feedback as a built-in, first-class concept
- **A**utomated: focus only on what actually requires your attention
- **T**rustworthy: support model assessment and oversight with traces and feedback; trustworthiness requires use-case-specific evaluation

## Why GreatAI?

There are other existing solutions aiming to facilitate this phase. [Amazon SageMaker](https://aws.amazon.com/sagemaker) and [Seldon Core](https://docs.seldon.ai/seldon-core-2) provide the most comprehensive suite of features. If you have the opportunity to use them, do that because they're great.

However, [research indicates](https://great-ai.schmelczer.dev) that professionals rarely use them. This may be due to their inherent setup and operational complexity. **GreatAI is designed to be as simple to use as possible.** Its straightforward, high-level API and sensible default configuration make it easy to start using. Despite its relative simplicity over Seldon Core, it still implements many of the [SE4ML best practices](https://se-ml.github.io), and thus, can meaningfully improve your deployment without requiring prohibitively great effort.

## [Learn more](https://great-ai.schmelczer.dev)

[Check out the full documentation here](https://great-ai.schmelczer.dev).

## Find `great-ai` on [PyPI](https://pypi.org/project/great-ai/)

Requires Python 3.12 or later, including Python 3.13.
With uv installed and your virtual environment active:

```sh
uv pip install great-ai
```

## Find `great-ai` on [DockerHub](https://hub.docker.com/repository/docker/schmelczera/great-ai)

```sh
docker run -p6060:6060 schmelczera/great-ai
```

## Contribute

Contributions are welcome.

### Install for development

```sh
uv venv --seed --python 3.13 .env
source .env/bin/activate
uv pip install --editable '.[dev]'
```

### Develop

```sh
scripts/format-python.sh great_ai docs tests
```

> Format code.

```sh
python3 -m pytest --doctest-modules --asyncio-mode=strict .
```

> Run tests.

```sh
mkdocs serve
```

> Serve documentation.

### Release

With `git`, `python3`, and `uv` installed, run from a clean `main` checkout:

```sh
scripts/release.sh 0.2.0
```

This bumps the version, builds, commits, tags, and pushes `main` and the tag
atomically. The tag triggers the PyPI and DockerHub workflows, which require
`PYPI_TOKEN`, `DOCKER_USERNAME`, and `DOCKER_PASSWORD` in Forgejo repository secrets.
