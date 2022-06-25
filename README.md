# **S**coutinScience **U**tilitie**S** for text processing [![Lint and test ScoutinScience utilities](https://github.com/ScoutinScience/platform/actions/workflows/sus-general.yaml/badge.svg)](https://github.com/ScoutinScience/platform/actions/workflows/sus-general.yaml)

> amogus

## Exports

- [clean](src/sus/clean.py)
- [unique](src/sus/unique.py)
- [parallel_map](src/sus/parallel_map.py)
- [match_names](src/sus/match_names/match_names.py)
- [evaluate_ranking](src/sus/evaluate_ranking/evaluate_ranking.py)
- [get_sentences](src/sus/get_sentences.py)

### Requires loading spacy model

> This is automatic but will require some time.

> Add this to the Dockerfile for caching the spaCy model:
>
> ```docker
> RUN pip install --no-cache-dir en-core-web-sm@https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.3.0/en_core_web_sm-3.3.0-py3-none-any.whl
> ```

- [publication TEI](src/sus/publication_tei/publication_tei.py)
- [lemmatize_text](src/sus/lemmatize_text.py)
- [lemmatize_token](src/sus/lemmatize_token.py)
- [spacy model (nlp)](src/sus/nlp.py)
- [filter_sentences](src/sus/matcher/filter_sentences.py)

## Development

- Optional booleans must have a default value of `False`.
- No imports in top-level `__init__.py`, in order to not load anything unnecessary automatically
- Should only be updated through a PR
