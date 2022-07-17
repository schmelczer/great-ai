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
FROM schmelczera/great-ai:v0.1.6

COPY requirements.txt ./
RUN pip install --no-cache-dir --requirement requirements.txt

COPY . ./

RUN large-file --backend s3 --secrets s3.ini --cache scibert-highlights

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
