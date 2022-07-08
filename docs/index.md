# Welcome to GreatAI

Applying AI is becoming increasingly easier but many case studies have shown that these applications are often deployed poorly. GreatAI helps you transform your prototype AI code into production-ready software. 

??? quote
    There is a need to consider and adapt well established SE practices which have been ignored or had a very narrow focus in ML literature.
    &mdash; [Meenu et al.](https://ieeexplore.ieee.org/abstract/document/9359253)


## Features

- [x] Save traces of each prediction including arguments and model version
- [x] Store models and data on shared infrastructure (MongoDB GridFS, S3-compatible storage, local-disk)
- [x] Scaffold REST API and OpenAPI schema for easy integration
- [x] Seamless support for `async` inference methods
- [x] Support calling remote GreatAI instances
- [x] Save feedback and merge it into the ground-truth database
- [x] Built-in parallelising for batch processing
- [x] Well-tested utilities for common NLP tasks (cleaning, language-tagging, etc.)
- [x] Dashboard for high-level overview and searching traces
- [x] Fully-typed API for IntelliSense support
- [x] Docker support for deployment
- [x] Auto-reload fro development

> Can be highly customised, including turning of in specific cases, and disabling the logging of sensitive data.

## Hello world

```
pip install great-ai
```

```python title="hello-world.py" 
from great_ai import GreatAI

@GreatAI.create  #(1) 
def hello_world(name: str) -> str:
    return f"Hello {name}!"
```

1.  `@GreatAI.create` wraps your `hello_world` function with a `GreatAI` instance. The function will behave very similarly but:
    1. its return value becomes a `Trace[str]`,
    2. it gets a `process_batch` method for supporting parallel execution,
    3. and it can be deployed using the `great-ai` command-line tool.


??? note
    In practice, `hello_world` could be an inference function of some AI/ML application.

```bash title="terminal" 
great-ai hello-world.py
```
> Navigate to [localhost:6060](http://127.0.0.1:6060/) in your browser.

<div style="display: flex; justify-content: space-evenly;" markdown>
![](media/hello-world-dashboard.png){ loading=lazy }

![](media/hello-world-docs.png){ loading=lazy }
</div>

!!! success
    Your GreatAI service is ready for production use. Many of the [SE4ML best-practices](https://se-ml.github.io/) are configured and implemented automatically. To have full control over your service and to understand what else you might need to do in your use case, continue reading this documentation.


## Why is this GREAT?

![scope of GreatAI](scope-simple.drawio.svg)

GreatAI fits between the prototype and deployment phase of your (or your organisation's) AI development lifecycle. This is highlighted with blue in the diagram. Here, a number of best practices can be automatically implemented concerning the following 5 aspects:

- **G**eneral: support for all kinds of Python libraries without restriction
- **R**obust: robust error-handling and well-tested utilities out-of-the-box 
- **E**nd-to-end: managing end-to-end feedback is a built-in, first-class concept
- **A**utomated: focus only on what actually requires your attention
- **T**rustworthy: deploy models that you and society can confidently trust

## Why GreatAI?

There are other existing solutions aiming to solve facilitate this phase. [Amazon SageMaker](https://aws.amazon.com/sagemaker/) and [Seldon Core](https://www.seldon.io/solutions/open-source-projects/core) provide the most comprehensive suite of features. If you have the opportunity use those, they're great.

However, research indicates that professionals rarely use them. This may be due to their inherent setup and operating complexity. GreatAI is designed to be as simple to use as possible. Its clear, high-level API and sensible default configuration makes it extremely easy to start using. Despite its relative simplicity over Seldon Core, it still implements many [best-practices](https://se-ml.github.io/), and thus, can meaningfully improve your deployment without too much effort.


<div style="display: flex; justify-content: space-evenly;" markdown>
[:fontawesome-brands-python: Find it on PyPI](https://pypi.org/project/great-ai/){ .md-button .md-button--primary }

[:fontawesome-brands-docker: Find it on DockerHub](https://hub.docker.com/repository/docker/schmelczera/great-ai){ .md-button .md-button--primary }
</div>
