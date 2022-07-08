# GreatAI

**work in progress, do not use!**

[![Test](https://github.com/ScoutinScience/great-ai/actions/workflows/test.yml/badge.svg)](https://github.com/ScoutinScience/great-ai/actions/workflows/check.yml)
[![Quality Gate Status](https://sonar.scoutinscience.com/api/project_badges/measure?project=great-ai&metric=alert_status)](https://sonar.scoutinscience.com/dashboard?id=great-ai)
[![Publish on PyPI](https://github.com/ScoutinScience/great-ai/actions/workflows/publish.yaml/badge.svg)](https://github.com/ScoutinScience/great-ai/actions/workflows/publish.yaml)
[![Publish on DockerHub](https://github.com/ScoutinScience/great-ai/actions/workflows/docker.yaml/badge.svg)](https://github.com/ScoutinScience/great-ai/actions/workflows/docker.yaml)
[![Downloads](https://pepy.tech/badge/great-ai/month)](https://pepy.tech/project/great-ai)


## Find `great-ai` on [DockerHub](https://hub.docker.com/repository/docker/schmelczera/great-ai)

```sh
docker run -p6060:6060 schmelczera/great-ai
```

Find the dashboard at [http://localhost:6060](http://localhost:6060/dashboard/).


## Find `great-ai` on [PyPI](https://pypi.org/project/great-ai/)

```sh
pip install great-ai
```

```python
from great_ai import GreatAI

@GreatAI.create
def hello_world(name: str) -> str:
    return f"Hello {name}!"
```
> Create a new file called `main.py`

Deploy by executing `python3 -m great-ai main.py`
> Or: `python3 -m great-ai main.py`

Find the dashboard at [http://localhost:6060](http://localhost:6060/dashboard/).

### Contribute


#### Install

```sh
pip install 'great-ai[dev]'
```

#### Documentation

```sh
mkdocs serve
```