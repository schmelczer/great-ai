# **S**coutinScience **U**tilitie**S** for text processing [![Lint and test ScoutinScience utilities](https://github.com/ScoutinScience/platform/actions/workflows/sus-general.yaml/badge.svg)](https://github.com/ScoutinScience/platform/actions/workflows/sus-general.yaml)

## Exports

- [clean](src/sus/clean.py)
- [unique](src/sus/unique.py)
- [parallel_map](src/sus/parallel_map.py)
- [lemmatize](src/sus/lemmatize.py)
- [evaluate_ranking](src/sus/evaluate_ranking/evaluate_ranking.py)
- [get_sentences](src/sus/get_sentences.py)

## Development

- Optional booleans must have a default value of `False`.
- No imports in top-level `__init__.py`, in order to not load anything unnecessary automatically
- Should only be updated through a PR
