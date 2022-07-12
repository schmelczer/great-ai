# How to deploy a GreatAI service

After [creating a GreatAI service](/how-to-guides/create-service) by wrapping your prediction function, and optionally [configuring it](/how-to-guides/configure-service), it's time to do some prediction.

Let's take the following example:

```python title="greeter.py"
from great_ai import GreatAI

@GreatAI.create
def greeter(your_name: str) -> str:
    return f'Hi {your_name}'
```

## One-off prediction

Even though `greeter` is now an instance of [GreatAI][great_ai.GreatAI], you can continue using it as a regular function.

```python
>>> greeter('Bob')
Trace[str]({'created': '2022-07-11T14:31:46.183764',
  'exception': None,
  'feedback': None,
  'logged_values': {'arg:your_name:length': 3, 'arg:your_name:value': 'Bob'},
  'models': [],
  'original_execution_time_ms': 0.0381,
  'output': 'Hi Bob',
  'tags': ['greeter', 'online', 'development'],
  'trace_id': '7c284fd7-7f0d-4464-b5f8-3ef126df34af'})
```

As you can see, the original return value is wrapped in a [Trace][great_ai.Trace] object (which is also persisted in your database of choice). You can access the original value under the `output` property.

## Online prediction

Likely, the main way you would like to expose your model is through an HTTP API. [@GreatAI.create][great_ai.GreatAI.create] scaffolds many REST API endpoints for your model and creates a [FastAPI](https://fastapi.tiangolo.com/){ target=_blank } app available under [GreatAI.app][great_ai.GreatAI]. This can be served using [uvicorn](https://www.uvicorn.org/){ target=_blank } or any other [ASGI server](https://asgi.readthedocs.io/en/latest/){ target=_blank }.

Since most ML code lives in [Jupyter](https://jupyter.org/){ target=_blank } notebooks, therefore, deploying a notebook containing the inference function is supported. To this end, `uvicorn` is wrapped by the `great-ai` command-line utility which, among others, takes care of feeding a notebook into `uvicorn`. It also supports auto-reloading.

### In development

```sh
great-ai greeter.py
```

!!! success
    Your model is accessible at [localhost:6060](http:/127.0.0.1:6060){ target=_blank }.

Some configuration options are also supported.

```sh
great-ai greeter.py --port 8000 --host 127.0.0.1 --timeout_keep_alive 10
```
??? note "More options"
    For more options (but no Notebook support), simply use [uvicorn](https://www.uvicorn.org/){ target=_blank } for starting your app (available at `greeter.app`).

### In production

There are three main approaches for deploying a GreatAI service.

#### Manual deployment

The app is run in *production-mode* if the value of the `ENVIRONMENT` environment variable is set to `production`.

```sh
ENVIRONMENT=production great-ai greeter.py
```

Simply run `ENVIRONMENT=production great-ai deploy.ipynb` in the command-line of a production machine.
> This is the crudest approach, however, it might be fitting for some contexts.

#### Containerised deployment

Run the notebook directly in a container or create a service for it using your favourite container orchestrator.

```sh
docker run -p 6060:6060 --volume `pwd`:/app --rm \
  schmelczera/great-ai deploy.ipynb
```
> You can replace ``pwd`` with the path to your code's folder.

#### Use a Platform-as-a-Service

Similarly to the previous approach, your code will run in a container. However, instead of manually managing it, you can just choose from a plethora of PaaS providers (such as [AWS ECS](https://aws.amazon.com/ecs/){ target=_blank }, [DO App platform](https://www.digitalocean.com/products/app-platform){ target=_blank }, [MLEM](https://mlem.ai/){ target=_blank }) that take a Docker image as a source and handle the rest of the deployment.

To this end, you can also create a custom Docker image. It is especially useful if you have third-party dependencies, such as [PyTorch](https://pytorch.org/){ target=_blank } or [TensorFlow](https://www.tensorflow.org/){ target=_blank }.

```Dockerfile
FROM schmelczera/great-ai:latest

# Remove this block if you don't have a requirements.txt
COPY requirements.txt ./   
RUN pip install --no-cache-dir --requirement requirements.txt

# If you store your models in S3 or GridFS, it may be a 
# good idea to cache them in the image so that you don't
# have to download it each time a container starts
RUN large-file --backend s3 --secrets s3.ini --cache my-domain-predictor

# Add you application code to the image
COPY . .

# The default ENTRYPOINT is great-ai, specify it's argument using CMD
CMD ["deploy.ipynb"]

```

## Batch prediction

Processing larger amounts of data on a single machine is made easy by the [GreatAI][great_ai.GreatAI]'s [process_batch][great_ai.GreatAI.process_batch] method. This relies on multiprocessing ([parallel_map][great_ai.utilities.parallel_map.parallel_map.parallel_map]) to take full advantage of all available CPU-cores.

```python
>>> greeter.process_batch(['Alice', 'Bob'])
[Trace[str]({'created': '2022-07-11T14:36:37.119183',
   'exception': None,
   'feedback': None,
   'logged_values': {'arg:your_name:length': 5, 'arg:your_name:value': 'Alice'},
   'models': [],
   'original_execution_time_ms':  0.1251,
   'output': 'Hi Alice',
   'tags': ['greeter', 'online', 'development'],
   'trace_id': '90ffa15f-e839-41c4-8e7a-3211168bc138'}),
 Trace[str]({'created': '2022-07-11T14:36:37.166659',
   'exception': None,
   'feedback': None,
   'logged_values': {'arg:your_name:length': 3, 'arg:your_name:value': 'Bob'},
   'models': [],
   'original_execution_time_ms':  0.0571,
   'output': 'Hi Bob',
   'tags': ['greeter', 'online', 'development'],
   'trace_id': 'f48e94c7-0815-48b3-a864-41349d3dae84'})]
```
