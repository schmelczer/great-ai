# GreatAI

**work in progress, do not use!**

[![Test](https://github.com/ScoutinScience/great_ai/actions/workflows/test.yml/badge.svg)](https://github.com/ScoutinScience/great_ai/actions/workflows/check.yml)
[![Quality Gate Status](https://sonar.scoutinscience.com/api/project_badges/measure?project=great-ai&metric=alert_status)](https://sonar.scoutinscience.com/dashboard?id=great_ai)
[![Publish on PyPI](https://github.com/ScoutinScience/great_ai/actions/workflows/publish.yaml/badge.svg)](https://github.com/ScoutinScience/great_ai/actions/workflows/publish.yaml)
[![Publish on DockerHub](https://github.com/ScoutinScience/great_ai/actions/workflows/docker.yaml/badge.svg)](https://github.com/ScoutinScience/great_ai/actions/workflows/docker.yaml)
[![Downloads](https://pepy.tech/badge/great_ai/month)](https://pepy.tech/project/great_ai)


## Find `great_ai` on [DockerHub](https://hub.docker.com/repository/docker/schmelczera/great_ai)

```sh
docker run -p6060:6060 schmelczera/great_ai
```

Find the dashboard at [http://localhost:6060](http://localhost:6060/dashboard/).


## Find `great_ai` on [PyPI](https://pypi.org/project/great_ai/)

```sh
pip install great_ai
```

```python
from great_ai import GreatAI

@GreatAI.create
def hello_world(name: str) -> str:
    return f"Hello {name}!"
```
> Create a new file called `main.py`

Deploy by executing `python3 -m great_ai main.py`

Find the dashboard at [http://localhost:6060](http://localhost:6060/dashboard/).

### Contribute

```sh
pip install 'great_ai[dev]'

```
