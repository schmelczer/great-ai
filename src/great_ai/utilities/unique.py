from typing import Any, Callable, Iterable, List


def unique(
    values: Iterable[Any], *, key: Callable[[Any], Any] = lambda v: v
) -> List[Any]:
    """Only keep first occurrences and maintain order"""

    key_values = {}
    for v in values:
        k = key(v)
        if k not in key_values:
            # dicts maintain insertion order: https://mail.python.org/pipermail/python-dev/2017-December/151283.html
            key_values[k] = v

    return list(key_values.values())
