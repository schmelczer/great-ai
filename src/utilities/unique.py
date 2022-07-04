from typing import Any, Callable, Iterable, List


def unique(
    values: Iterable[Any], *, key: Callable[[Any], Any] = lambda v: v
) -> List[Any]:
    """Only keep first occurrences while maintaining original order.

    The equality check used for deduplication can be overridden using the `key` argument.

    Examples:
        >>> unique([1, 1, 5, 3, 3])
        [1, 5, 3]
        >>> unique([{'a': 1, 'b': 2}, {'a': 1, 'b': 3}], key=lambda v: v['a'])
        [{'a': 1, 'b': 2}]
        >>> unique([{'a': 1, 'b': 2}, {'a': 1, 'b': 3}], key=lambda v: v['b'])
        [{'a': 1, 'b': 2}, {'a': 1, 'b': 3}]
    """

    key_values = {}
    for v in values:
        k = key(v)
        if k not in key_values:
            # dicts maintain insertion order: https://mail.python.org/pipermail/python-dev/2017-December/151283.html
            key_values[k] = v

    return list(key_values.values())
