# Installation guide

Provided you already have [Python3](https://www.python.org/downloads/){ target=_blank } (and pip) installed, simply execute:

```sh
pip install great-ai
```
> Python 3.8 or later is required.

This will work on all major operating systems.

## Command-line tools

After installation, `great-ai` and `large-file` are available as commands. The former is required for deploying your application while the latter lets you manage models and datasets from your terminal.

!!! warning "Windows"
    On Windows, you might encounter a similar ==warning== from `pip`:
    >  WARNING: The scripts great-ai.exe, great_ai.exe, large-file.exe and large_file.exe are installed in 'C:\Users\...\Scripts' which is not on PATH.
    > Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.

    This means that `great-ai.exe` and `large-file.exe` are not in your `PATH`. Either add their containing directory ('C:\Users\...\Scripts' in this case) to your `PATH` or use `python3 -m great_ai` and `python3 -m great_ai.large_file` instead of the exe-s.
