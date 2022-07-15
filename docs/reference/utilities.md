# Utilities

```python
from great_ai.utilities import *
```

## NLP tools

Well-tested tools that can be used in production with confidence. The toolbox of feature-extraction functions is expected to grow to cover other domains as well.

::: great_ai.utilities.clean
::: great_ai.utilities.get_sentences
::: great_ai.utilities.language.predict_language
::: great_ai.utilities.language.english_name_of_language
::: great_ai.utilities.language.is_english
::: great_ai.utilities.evaluate_ranking.evaluate_ranking

## Parallel processing

Multiprocessing and multithreading-based parallelism with support for `async` functions. Its main purpose is to implement [great_ai.GreatAI.process_batch][], however, the parallel processing functions are also convenient for covering other types of mapping needs with a friendlier API than [joblib](https://joblib.readthedocs.io/en/latest/parallel.html){ target=_blank } or [multiprocess](https://pypi.org/project/multiprocess/){ target=_blank }.

::: great_ai.utilities.simple_parallel_map
    options:
        show_root_heading: true
::: great_ai.utilities.parallel_map.parallel_map
::: great_ai.utilities.threaded_parallel_map
    options:
        show_root_heading: true

## Composable parallel processing

Because both [threaded_parallel_map][great_ai.utilities.parallel_map.threaded_parallel_map.threaded_parallel_map] and [parallel_map][great_ai.utilities.parallel_map.parallel_map.parallel_map] have a streaming interface, it is easy to compose them and end up with, for example, a process for each CPU core with its own thread-pool or event-loop. Longer pipelines are also easy to imagine. The chunking methods help in these compositions.

::: great_ai.utilities.chunk
::: great_ai.utilities.unchunk

## Operations

::: great_ai.utilities.ConfigFile
    options:
        show_root_heading: true
    
::: great_ai.utilities.get_logger
    options:
        show_root_heading: true
