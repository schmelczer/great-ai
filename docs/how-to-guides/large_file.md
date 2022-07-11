# How to use LargeFile

Storing, versioning, and downloading files from S3 made as easy as using `open()` in Python. Caching included.

## Motivation

Oftentimes, especially when working with data-heavy applications, large files can proliferate in a repository. Version controlling them is an obvious next step, however, GitHub's git LFS implementation [doesn't support the deletion](https://docs.github.com/en/repositories/working-with-files/managing-large-files/removing-files-from-git-large-file-storage#git-lfs-objects-in-your-repository) of large files, making it easy for them to eat-up the LFS quota and explode the size of your repos.

## Solution

```
pip install open-large
```

### Simple example

```python
from great_ai.large_file import LargeFileS3

LargeFileS3.configure_credentials({
    "aws_region_name": "your_region_like_eu-west-2",
    "aws_access_key_id": "YOUR_ACCESS_KEY_ID",
    "aws_secret_access_key": "YOUR_VERY_SECRET_ACCESS_KEY",
    "large_files_bucket_name": "create_a_bucket_and_put_its_name_here",
})

# Creates a new version and deletes the older version leaving the 3 most recently used intact
with LargeFileS3("test.txt", "w", keep_last_n=3) as f:
    for i in range(100000):
        f.write('test\n')

# By default the latest version is returned
# but an optional `version` keyword argument can be provided as well
with LargeFileS3("test.txt", "r") as f:
    print(f.readlines()[0])
```

> Automatically creates a file, writes to it, uploads it to S3, and then queries the most recent version of it.
> In this case, the latest version is already in the local cache, no download is required.

### More details

`LargeFile` behaves like an opened file (in the background it is a temp file after all). Binary reading and writing is supported along with the [different keywords](https://docs.python.org/3/library/functions.html#open) `open()` accepts.

The local cache can be configured with these properties:

```python
LargeFile.cache_path = Path('.cache')
LargeFile.max_cache_size = "30 GB"
```

#### I only need a path

In case you only need a path to the "remote" file, this pattern can be applied:

```python
path_to_model = LargeFile("folder-of-my-bert-model", version=31).get()
```

> This will first download the file/folder into your local cache folder. Then, it returns a `Path` object to the local version. Which can be turned into a string with `str(path_to_model)`.

The same approach works for uploads:

```python
LargeFile("folder-of-my-bert-model").push('path_to_local/folder_or_file')
```

> This way, both regular files and folders can be handled. The uploaded file is called **folder-of-my-bert-model**, the local name is ignored.

Lastly, all version of the remote object can be deleted by calling `LargeFile("my-file").delete()`. It will still reside in your local cache afterwards, its deletion will happen next time your local cache has to be pruned.

### Command-line example

The package can be used as a module from the command-line to give you more flexibility.

#### Setup

Create an .ini file (or use _~/.aws/credentials_). It may look like this:

```ini
aws_region_name = your_region_like_eu-west-2
aws_access_key_id = YOUR_ACCESS_KEY_ID
aws_secret_access_key = YOUR_VERY_SECRET_ACCESS_KEY
large_files_bucket_name = my_large_files
endpoint_url = this is optional, for backblaze, use this: https://s3.us-west-002.backblazeb2.com
```

> Just like in [example secrets](example_secrets.ini).

#### Print the expected options

```sh
python3 -m large_file --help
```

#### Upload some files

```sh
python3 -m large_file --backend s3 --secrets secrets.ini --push my_first_file.json folder/my_second_file my_folder
```

> Only the filename is used as the S3 name, the rest of the path is ignored.

#### Download some files to the local cache

This can be useful when building a Docker image for example. This way, the files can already reside inside the container and need not be downloaded later.

```sh
python3 -m large_file --backend s3 -secrets ~/.aws/credentials --cache my_first_file.json:3 my_second_file my_folder:0
```

> Versions may be specified by using `:`-s.

#### Delete remote files

```sh
python3 -m large_file --backend s3 --secrets ~/.aws/credentials --delete my_first_file.json
```
