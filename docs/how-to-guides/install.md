# Installation guide

Provided you already have [Python3](https://www.python.org/downloads/){ target=_blank } (and pip) installed, simply execute:

```sh
pip install great-ai
```
> Python 3.7 or later is required.

This will work on all major operating systems.

## Google Colab

In order to use GreatAI in [Google Colab](https://colab.research.google.com){ target=_blank }, you need to downgrade `pyyaml` to a Colab compatible version. [See related StackOverflow question](https://stackoverflow.com/questions/69564817/typeerror-load-missing-1-required-positional-argument-loader-in-google-col){ target=_blank }.

```sh
pip install great-ai pyyaml==5.4.1
```
> This will make GreatAI work in Colab.

## Command-line tools

After installation, `great-ai` and `large-file` are available as commands. The former is required for deploying your application, while the latter lets you manage models and datasets from your terminal.

??? note "Snakes & kebabs"
    The library is called `great-ai`; therefore, its command-line entry point is also called `great-ai`. However, Python module names cannot contain hyphens, that's why you have to `import great_ai` with an underscore. The `great-ai` CLI tool is also available as `python3 -m great_ai`.

    To help with the confusion, a CLI executable called `great_ai` (and `large_file`) are also installed. Thus, if you prefer, you can always refer to GreatAI using its underscored name variant (`great_ai`).

!!! warning "Windows"
    On Windows, you might encounter a similar warning from `pip`:
    >  `WARNING: The scripts great-ai.exe, great_ai.exe, large-file.exe and large_file.exe are installed in 'C:\Users\...\Scripts', which is not on PATH.`
    
    > `Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.`

    This means that `great-ai.exe` and `large-file.exe` are not in your `PATH`. Either add their containing directory ('C:\Users\...\Scripts' in this case) to your `PATH` or use `python3 -m great_ai` and `python3 -m great_ai.large_file` instead of the exe-s.

## Update

If you wish to update to the latest version, execute:

```sh
pip install --upgrade great-ai
```

## Bleeding edge

You can also install the latest (usually unreleased) version from GitHub.

```sh
pip install --upgrade git+https://github.com/schmelczer/great-ai.git
```
> Python 3.7 or later is required.
