<div style="display: flex; justify-content: space-between; align-items: center;">
    <h1 style="margin: 0">Overview of GreatAI</h1>
    <img  src="media/logo.png" width=80>
</div>

[![PyPI version](https://badge.fury.io/py/great-ai.svg)](https://badge.fury.io/py/great-ai)
[![Downloads](https://pepy.tech/badge/great-ai/month)](https://pepy.tech/project/great-ai)
[![Docker Pulls](https://img.shields.io/docker/pulls/schmelczera/great-ai)](https://hub.docker.com/repository/docker/schmelczera/great-ai)
[![Test](https://github.com/schmelczer/great-ai/actions/workflows/test.yml/badge.svg)](https://github.com/schmelczer/great-ai/actions/workflows/test.yml)
[![Sonar line coverage](https://sonar.scoutinscience.com/api/project_badges/measure?project=great-ai&metric=coverage)](https://sonar.scoutinscience.com/dashboard?id=great-ai)
[![Sonar LoC](https://sonar.scoutinscience.com/api/project_badges/measure?project=great-ai&metric=ncloc)](https://sonar.scoutinscience.com/dashboard?id=great-ai)

Applying AI is becoming increasingly easier, but many case studies have shown that these applications are often deployed poorly. This may lead to suboptimal performance and to introducing [unintended biases](https://en.wikipedia.org/wiki/Weapons_of_Math_Destruction){ target=_blank }. GreatAI helps fix this by allowing you to ==easily transform your prototype AI code into production-ready software==.

??? quote "Case studies"
    "There is a need to consider and adapt well established SE practices which have been ignored or had a very narrow focus in ML literature."
    &mdash; [John et al.](https://ieeexplore.ieee.org/abstract/document/9359253){ target=_blank }

    "Finally, we have found that existing tools to aid Machine Learning development do not address the specificities of different projects, and thus, are seldom adopted by teams." &mdash; [Haakman et al.](https://link.springer.com/article/10.1007/s10664-021-09993-1){ target=_blank }

    "Because a mature system might end up being (at most) 5% machine learning code and (at least) 95% glue code, it may be less costly to create a clean native solution rather than re-use a generic package." &mdash; [Sculley et al.](https://www.researchgate.net/profile/Todd-Phillips/publication/319769912_Hidden_Technical_Debt_in_Machine_Learning_Systems/links/61e716d68d338833e37a7fd6/Hidden-Technical-Debt-in-Machine-Learning-Systems.pdf){ target=_blank }

    "For example, practice 25 is very important for "Traceability", yet relatively weakly adopted. We expect that the results from this type of analysis can, in the future, provide useful guidance for practitioners in terms of aiding them to assess their rate of adoption for each practice and to create roadmaps for improving their processes.  &mdash; [Serban et al.](https://dl.acm.org/doi/abs/10.1145/3382494.3410681?casa_token=uCFz0dtDR6gAAAAA:4_8OMJ-5njwopYkB1KSGAu9JfbNq4nfa8LRE0fj84ckjfo-GgtcYQivZTGxal3M4haoA8r_xwpw){ target=_blank }

## Features

- [x] Save prediction traces of each prediction, including arguments and model versions
- [x] Save feedback and merge it into a ground-truth database
- [x] Version and store models and data on shared infrastructure *(MongoDB GridFS, S3-compatible storage, shared volume)*
- [x] Automatically scaffolded custom REST API (and OpenAPI schema) for easy integration
- [x] Input validation
- [x] Sensible cache-policy
- [x] Graceful error handling
- [x] Seamless support for both synchronous and asynchronous inference methods
- [x] Easy integration with remote GreatAI instances
- [x] Built-in parallelisation (with support for multiprocessing, async, and mixed modes) for batch processing
- [x] Well-tested utilities for common NLP tasks (cleaning, language-tagging, sentence-segmentation, etc.)
- [x] A simple, unified configuration interface
- [x] Fully-typed API for [Pylance](https://github.com/microsoft/pylance-release){ target=_blank } and [MyPy](http://mypy-lang.org){ target=_blank } support
- [x] Auto-reload for development
- [x] Docker support for deployment
- [x] Deployable Jupyter Notebooks
- [x] Dashboard for online monitoring and analysing traces
- [x] Active support for Python 3.7, 3.8, 3.9, and 3.10

## Roadmap

- [ ] Prometheus & Grafana integration
- [ ] Well-tested feature extraction code for non-NLP data
- [ ] Support for direct file input
- [ ] Support for PostgreSQL

## Hello world

```sh
pip install great-ai
```

```python title="demo.py" 
from great_ai import GreatAI

@GreatAI.create  #(1) 
def greeter(name: str) -> str:  #(2) 
    return f"Hello {name}!"
```

1.  `@GreatAI.create` wraps your `greeter` function with a `GreatAI` instance. The function will behave very similarly but:
    1. its return value becomes a `Trace[str]`,
    2. it gets a `process_batch` method for supporting parallel execution,
    3. and it can be deployed using the `great-ai` command-line tool.

2.  [Typing functions](https://docs.python.org/3/library/typing.html){ target=_blank } is recommended in general, however, not required for GreatAI to work.

??? note
    In practice, `greeter` could be an inference function of some AI/ML application. But it could also just wrap a black-box solution of some SaaS. Either way, it is [imperative to have continuous oversight](https://digital-strategy.ec.europa.eu/en/library/ethics-guidelines-trustworthy-ai){ target=_blank } of the services you provide and the data you process, especially in the context of AI/ML applications.

```sh title="terminal" 
great-ai demo.py
```
> Navigate to [localhost:6060](http://127.0.0.1:6060) in your browser.

![demo screen capture](media/demo.gif){ loading=lazy }

!!! success
    Your GreatAI service is ready for production use. Many of the [SE4ML best practices](https://se-ml.github.io){ target=_blank } are configured and implemented automatically. To have full control over your service and to understand what else you might need to do in your use case, continue reading this documentation.

## Why is this GREAT?

![scope of GreatAI](media/scope-simple.drawio.svg)

GreatAI fits between the prototype and deployment phases of your (or your organisation's) AI development lifecycle. This is highlighted in blue in the diagram. Here, several best practices can be automatically implemented, aiming to achieve the following attributes:

- **G**eneral: use any Python library without restriction
- **R**obust: have error-handling and well-tested utilities out-of-the-box 
- **E**nd-to-end: utilise end-to-end feedback as a built-in, first-class concept
- **A**utomated: focus only on what actually requires your attention
- **T**rustworthy: deploy models that you and society can confidently trust

## Why GreatAI?

There are other existing solutions aiming to facilitate this phase. [Amazon SageMaker](https://aws.amazon.com/sagemaker){ target=_blank } and [Seldon Core](https://www.seldon.io/solutions/open-source-projects/core){ target=_blank } provide the most comprehensive suite of features. If you have the opportunity to use them, do that because they're great.

However, research indicates that professionals rarely use them. This may be due to their inherent setup and operational complexity. ==GreatAI is designed to be as simple to use as possible.== Its straightforward, high-level API and sensible default configuration make it extremely easy to start using. Despite its relative simplicity over Seldon Core, it still implements many of the [SE4ML best practices](https://se-ml.github.io){ target=_blank }, and thus, can meaningfully improve your deployment without requiring prohibitively great effort.


<div style="display: flex; justify-content: space-evenly; flex-wrap: wrap;" markdown>
[:fontawesome-brands-python: Find it on PyPI](https://pypi.org/project/great-ai){ .md-button .md-button--primary }

[:fontawesome-brands-docker: Find it on DockerHub](https://hub.docker.com/repository/docker/schmelczera/great-ai){ .md-button .md-button--primary }

[:fontawesome-solid-laptop-code: Check out the tutorial](/tutorial){ .md-button .md-button--primary }
</div>

## Production use

GreatAI has been battle-tested on the core platform services of [ScoutinScience](https://www.scoutinscience.com/){ target=_blank }.

[![ScoutinScience logo](media/scoutinscience.svg#only-light){ loading=lazy }
![ScoutinScience logo](media/scoutinscience-white.svg#only-dark){ loading=lazy }](https://www.scoutinscience.com/){ target=_blank }
