# ![logo](docs/media/favicon.ico) GreatAI
 
[![Sonar line coverage](https://sonar.scoutinscience.com/api/project_badges/measure?project=great-ai&metric=coverage)](https://sonar.scoutinscience.com/dashboard?id=great-ai)
[![Sonar LoC](https://sonar.scoutinscience.com/api/project_badges/measure?project=great-ai&metric=ncloc)](https://sonar.scoutinscience.com/dashboard?id=great-ai)
[![Test](https://github.com/schmelczer/great-ai/actions/workflows/test.yml/badge.svg)](https://github.com/schmelczer/great-ai/actions/workflows/test.yml)
[![PyPI version](https://badge.fury.io/py/great-ai.svg)](https://badge.fury.io/py/great-ai)
[![Downloads](https://pepy.tech/badge/great-ai/month)](https://pepy.tech/project/great-ai)
![Docker Pulls](https://img.shields.io/docker/pulls/schmelczera/great-ai)

GreatAI helps you easily transform your prototype AI code into production-ready software.
[Check out the full documentation here](https://great-ai.scoutinscience.com).

```sh
pip install great-ai
```

> Create a new file called `main.py`

```python
from great_ai import GreatAI

@GreatAI.create
def hello_world(name: str) -> str:
    return f"Hello {name}!"
```

Start it by executing `great-ai main.py`, find the dashboard at [http://localhost:6060](http://localhost:6060/dashboard).

![dashboard](/docs/media/hello-world-dashboard.png)

That's it. Your GreatAI service is ready for production use. Many of the [SE4ML best-practices](https://se-ml.github.io) are configured and implemented automatically (of course, these can be customised as well).

## Why is this GREAT?

![scope of GreatAI](docs/media/scope-simple.drawio.svg)

GreatAI fits between the prototype and deployment phases of your (or your organisation's) AI development lifecycle. This is highlighted with blue in the diagram. Here, a number of best practices can be automatically implemented aiming to achieve the following attributes:

- **G**eneral: use any Python library without restriction
- **R**obust: have error-handling and well-tested utilities out-of-the-box 
- **E**nd-to-end: utilise end-to-end feedback as a built-in, first-class concept
- **A**utomated: focus only on what actually requires your attention
- **T**rustworthy: deploy models that you and society can confidently trust

## Why GreatAI?

There are other, existing solutions aiming to facilitate this phase. [Amazon SageMaker](https://aws.amazon.com/sagemaker) and [Seldon Core](https://www.seldon.io/solutions/open-source-projects/core) provide the most comprehensive suite of features. If you have the opportunity use those, do that because they're great.

However, [research indicates](https://great-ai.scoutinscience.com) that professionals rarely use them. This may be due to their inherent setup and operating complexity. **GreatAI is designed to be as simple to use as possible.** Its clear, high-level API and sensible default configuration makes it extremely easy to start using. Despite its relative simplicity over Seldon Core, it still implements many of the [SE4ML best-practices](https://se-ml.github.io), and thus, can meaningfully improve your deployment without requiring prohibitively large effort.

## Find `great-ai` on [DockerHub](https://hub.docker.com/repository/docker/schmelczera/great-ai)

```sh
docker run -p6060:6060 schmelczera/great-ai
```

## Learn more

[Check out the documentation](https://great-ai.scoutinscience.com).

## Contribute

Contributions are welcome.

### Install for development

```sh
python3 -m venv --copies .env
source .env/bin/activate
python3 -m pip install flit
python3 -m flit install --symlink --deps=all
```

### Serve documentation

```sh
mkdocs serve --dirtyreload
```
