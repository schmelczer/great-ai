# How to configure GreatAI

GreatAI aims to provide reasonable defaults wherever possible. The current configuration is always prominently displayed (and updated) on the dashboard and in the command-line startup banner.

## Using [great_ai.configure][]

You can override any of the default settings by calling [great_ai.configure][]. If you don't call `configure`, the default settings are applied on the first call to most `great-ai` functions.

!!! warning
    You must call [great_ai.configure][] before calling (or decorating with) any other `great-ai` function. However, importing other functions before calling [great_ai.configure][] is permitted.

```python title="configure-demo.py"
from great_ai import configure, RouteConfig
import logging

configure(
    version='1.0.0',
    log_level=logging.INFO,
    seed=2,
    should_log_exception_stack=False, 
    prediction_cache_size=0,  #(1)
    disable_se4ml_banner=True,
    dashboard_table_size=200,
    route_config=RouteConfig(  #(2)
        feedback_endpoints_enabled=False,
        dashboard_enabled=False
    )
)
```

1.  Completely disable caching.
2.  The unspecified routes are enabled by default.

## Using remote storage

The only aspect that cannot be automated is choosing the backing storage for the database and file storage.

Right now, you have 3 options for storing the models and large datasets: [LargeFileLocal][great_ai.large_file.LargeFileLocal], [LargeFileMongo][great_ai.large_file.LargeFileMongo], and [LargeFileS3][great_ai.large_file.LargeFileS3].

Without explicit configuration, [LargeFileLocal][great_ai.large_file.LargeFileLocal] is selected by default. This one still version-controls your files but it only stores them in a local path.

!!! important
    If your working directory contains a `mongo.ini` or `s3.ini` file, an attempt is made to auto-configure [LargeFileMongo][great_ai.large_file.LargeFileMongo] or [LargeFileS3][great_ai.large_file.LargeFileS3] respectively.

To use [LargeFileMongo][great_ai.large_file.LargeFileMongo] or [LargeFileS3][great_ai.large_file.LargeFileS3] explicitly, configure them before calling any other `great-ai` function.

### S3-compatible

```toml title="s3.ini"
aws_region_name = eu-west-2
aws_access_key_id = MY_AWS_ACCESS_KEY  # ENV:MY_AWS_ACCESS_KEY would also work
aws_secret_access_key = MY_AWS_SECRET_KEY
large_files_bucket_name = bucket-for-models
```

```python title="use-s3.py"
from great_ai.large_file import LargeFileS3
from great_ai import save_model

LargeFileS3.configure_credentials_from_file('s3.ini') #(1)

model = [4, 3]
save_model(model, 'my-model')
```

1.  This line isn't strictly necceseary because if `s3.ini` (or `mongo.ini`) is available in the current working directory, they are automatically used to configure their respective LargeFile implementations/databases.

??? note "Departing from AWS"
    With the `aws_endpoint_url` argument, it is possible to use any other S3-compatible service such as [Backblaze](https://www.backblaze.com/){ target=_blank }. In that case, it would be `aws_endpoint_url=https://s3.us-west-002.backblazeb2.com`.

### GridFS

[GridFS](https://www.mongodb.com/docs/manual/core/gridfs/#:~:text=GridFS%20is%20a%20specification%20for,chunk%20as%20a%20separate%20document.){ target=_blank } specifies how to store files in MongoDB. The official MongoDB server and many compatible implementations support it.

```toml title="mongo.ini"
MONGO_CONNECTION_STRING=mongodb://localhost:27017  # this is the default value
# if `MONGO_CONNECTION_STRING` is specified, this default is overridden
MONGO_CONNECTION_STRING=ENV:MONGO_CONNECTION_STRING

MONGO_DATABASE=my-database  # it is automatically created if doesn't exist
```

```python title="use-mongo.py"
from great_ai.large_file import LargeFileMongo
from great_ai import save_model

LargeFileMongo.configure_credentials_from_file('mongo.ini')

model = [4, 3]
save_model(model, 'my-model')
```

!!! note "Simplifying config files"
    You can combine `mongo.ini` or `s3.ini` with your application's config file because the unneeded keys are ignored by the `configure_credentials_from_file` method.

## Using a database

By default, a thread-safe version of [TinyDB](https://tinydb.readthedocs.io/en/latest/){ target=_blank } is utilised for saving the prediction traces into a local file. Unfortunately, for most production needs, this method is not suitable.

### MongoDB

At the moment, only MongoDB is supported as a production-ready `TracingDatabase`. In order to use it, you have to either place a file named `mongo.ini` in your working directory, or explicitly call [MongoDbDriver.configure_credentials_from_file][great_ai.MongoDbDriver] or [MongoDbDriver.configure_credentials][great_ai.MongoDbDriver.configure_credentials].
