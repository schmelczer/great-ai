# How to use LargeFiles

The functions [save_model][great_ai.use_model] and [@use_model][great_ai.use_model] wrap LargeFile instances. Hence, besides configuring [LargeFile](/reference/large-file), users have few reasons to use LargeFiles directly.

## Motivation

Often, especially when working with data-heavy applications, large files can proliferate in a repository. Version controlling them is an obvious next step. However, GitHub's git LFS implementation [doesn't support deleting](https://docs.github.com/en/repositories/working-with-files/managing-large-files/removing-files-from-git-large-file-storage#git-lfs-objects-in-your-repository) large files, making it easy for them to eat-up the LFS quota and explode the size of your repos.

[DVC](https://dvc.org/) is a viable alternative; however, it requires users to learn to use one more CLI tool.

??? note "Using LargeFile-s directly (usually not needed)"
    LargeFile doesn't require users to learn too much new. It is a nearly exact copy of Python's built-in `open()` function, with which users are undoubtedly already familiar.

    ## Simple example

    ```python
    from great_ai.large_file import LargeFileS3

    LargeFileS3.configure_credentials({
        "aws_region_name": "your_region_like_eu-west-2",
        "aws_access_key_id": "YOUR_ACCESS_KEY_ID",
        "aws_secret_access_key": "YOUR_VERY_SECRET_ACCESS_KEY",
        "large_files_bucket_name": "create_a_bucket_and_put_its_name_here",
    })

    # Creates a new version and deletes the older version 
    # leaving the three most recently used intact
    with LargeFileS3("test.txt", "w", keep_last_n=3) as f:
        for i in range(100000):
            f.write('test\n')

    # The latest version is returned by default
    # but an optional `version` keyword argument can be provided as well
    with LargeFileS3("test.txt", "r") as f:  #(1)
        print(f.readlines()[0])
    ```

    1. The latest version is already in the local cache; no download is required.

    ### More details

    `LargeFile` behaves like an opened file (in the background, it is a temp file after all). Binary reads and writes are supported along with the [different keywords `open()` accepts](https://docs.python.org/3/library/functions.html#open){ target=_blank }.

    The local cache can be configured with these properties:

    ```python
    LargeFileS3.cache_path = Path('.cache')
    LargeFileS3.max_cache_size = "30 GB"
    ```

    #### I only need a path

    In case you only need a path to the (proxy of the) remote file, this pattern can be applied:

    ```python
    path_to_model = LargeFileS3("folder-of-my-bert-model", version=31).get()
    ```

    > This will first download the file/folder into your local cache folder. Then, it returns a `Path` object to the local version. Which can be turned into a string with `str(path_to_model)`.

    The same approach works for uploads:

    ```python
    LargeFileS3("folder-of-my-bert-model").push('path_to_local/folder_or_file')
    ```

    > This way, both regular files and folders can be handled. The uploaded file is called **folder-of-my-bert-model**, the local name is ignored.

    Lastly, all version of the remote object can be deleted by calling `LargeFileS3("my-file").delete()`. It will still reside in your local cache afterwards; its deletion will happen next time your local cache has to be pruned.

## From the command-line 

The main reason for using the `large-file` or `python3 -m great_ai.large_file` commands is to upload or download models from the terminal. For example, when building a docker image, it is best practice to cache the referred models.

### Setup

Create an .ini file (or use *~/.aws/credentials*). It may look like this:

```ini
aws_region_name = your_region_like_eu-west-2
aws_access_key_id = YOUR_ACCESS_KEY_ID
aws_secret_access_key = YOUR_VERY_SECRET_ACCESS_KEY
large_files_bucket_name = my_large_files
```

### Upload some files

```sh
large-file --backend s3 --secrets secrets.ini \
    --push my_first_file.json folder/my_second_file my_folder
```

> Only the filename is used as the S3 name; the rest of the path is ignored.

!!! important "Using MongoDB"
    The possible values for `--backend` are `s3`, `mongo`, and `local`. The latter doesn't need credentials. It only versions and stores your files in a local folder. MongoDB, on the other hand, requires a `mongo_connection_string` and a `mongo_database` to be specified. For storing large files, it uses the [GridFS](https://www.mongodb.com/docs/manual/core/gridfs){ target=_blank } specification.

### Download some files to the local cache

This can be useful when building a Docker image, for example. This way, the files can already reside inside the container and need not be downloaded later.

```sh
large-file --backend s3 --secrets ~/.aws/credentials \
    --cache my_first_file.json:3 my_second_file my_folder:0
```

> Versions may be specified by using `:`-s.

### Delete remote files

```sh
large-file --backend s3 --secrets ~/.aws/credentials \
    --delete my_first_file.json
```
