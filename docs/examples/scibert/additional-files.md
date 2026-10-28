# Additional files in the repository

In order to give you a smooth experience while comprehending this example, all non-notebook files are presented on this page in one place. In reality, these files should be in your project's top-level directory.

## config.ini

```ini title="config.ini"
ENVIRONMENT = DEVELOPMENT
ENVIRONMENT = ENV:ENVIRONMENT

MONGO_CONNECTION_STRING=ENV:MONGO_CONNECTION_STRING
MONGO_DATABASE=highlights

AWS_REGION_NAME = eu-west-2
AWS_ACCESS_KEY_ID = MY_DEFAULT_AWS_ACCESS_KEY_ID_FOR_DEVELOPMENT
AWS_SECRET_ACCESS_KEY = MY_DEFAULT_AWS_SECRET_ACCESS_KEY_FOR_DEVELOPMENT
LARGE_FILES_BUCKET_NAME = my-orgs-large-files

AWS_REGION_NAME = ENV:AWS_REGION_NAME
AWS_ACCESS_KEY_ID = ENV:AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = ENV:AWS_SECRET_ACCESS_KEY
LARGE_FILES_BUCKET_NAME = ENV:LARGE_FILES_BUCKET_NAME
```

> All necessary configuration which is read by [great_ai.utilities.ConfigFile][]. This will resolve values starting with `ENV:` from your environment variables.

## requirements.txt

```requirements.txt title="requirements.txt"
torch==1.12.0
transformers==4.20.1
numpy==1.23.0
```

> Usually, it is recommended to pin (freeze) the library versions on which we depend. This file is referenced by the [Dockerfile](#dockerfile).

## Dockerfile

```Dockerfile title="Dockerfile"
# syntax=docker/dockerfile:1
FROM schmelczera/great-ai:v0.1.6

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

COPY requirements.txt ./
RUN uv pip install --system --no-cache --requirement requirements.txt

RUN --mount=type=secret,id=config,target=/run/secrets/config.ini,required=true \
    large-file --backend s3 --secrets /run/secrets/config.ini --cache scibert-highlights

COPY . ./

CMD ["deploy.ipynb"]
```

> This is used by the CD pipeline to create the production deployment of the service.

## .dockerignore

```dockerignore title=".dockerignore"
.cache
.git
data
.gitignore
.env
config.ini
s3.ini
mongo.ini
.vscode
.dockerignore
Dockerfile
.mypy_cache
.gitignore
**/__pycache__
**/.DS_Store
README.md
```

> It is useful not to send, for example, the `.cache` folder used by LargeFile to the docker daemon; this will speed up your local build times substantially.

!!! Note ".gitignore"
    A very similar looking `.gitignore` file should also be present.

## Build and run with model caching

Use [Docker BuildKit secrets](https://docs.docker.com/build/building/secrets/) to make the build configuration available to the model-cache command without copying credentials into the image. The application's `config.ini` above also refers to runtime environment variables such as `MONGO_CONNECTION_STRING`. For the build, prepare a separate `config.ini` outside the project, for example at `/secure/build/config.ini`, containing only these four S3 settings with your actual values:

```ini title="/secure/build/config.ini"
AWS_REGION_NAME = eu-west-2
AWS_ACCESS_KEY_ID = YOUR_BUILD_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = YOUR_BUILD_SECRET_ACCESS_KEY
LARGE_FILES_BUCKET_NAME = my-orgs-large-files
```

Use concrete values here: the build container does not inherit your shell's environment for resolving `ENV:` entries. After uploading `scibert-highlights` in the training notebook, build from the project's top-level directory:

```sh
DOCKER_BUILDKIT=1 docker build --no-cache --progress=plain \
  --secret id=config,src=/secure/build/config.ini --tag scibert-highlights .
```

`--no-cache` makes Docker run the model-cache step even if a previous image layer exists. The model stays in the image, while the secret mount is removed after that step. The `.dockerignore` above also prevents the application's `config.ini` from being included by `COPY . ./`.

At runtime, mount the application's `config.ini` and pass the environment variables it references from your configured shell:

```sh
docker run --rm -p 6060:6060 \
  --mount type=bind,source="$(pwd)/config.ini",target=/app/config.ini,readonly \
  --env MONGO_CONNECTION_STRING --env AWS_REGION_NAME \
  --env AWS_ACCESS_KEY_ID --env AWS_SECRET_ACCESS_KEY \
  --env LARGE_FILES_BUCKET_NAME scibert-highlights
```
