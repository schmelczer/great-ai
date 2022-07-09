from typing import Awaitable, Callable, List, Optional, Sequence, TypeVar, Union

from tqdm.cli import tqdm

from .parallel_map import parallel_map

T = TypeVar("T")
V = TypeVar("V")


def simple_parallel_map(
    func: Callable[[T], Union[V, Awaitable[V]]],
    input_values: Sequence[T],
    *,
    chunk_size: Optional[int] = None,
    concurrency: Optional[int] = None,
) -> List[V]:
    input_values = list(input_values)  # in case the input is mistakenly not a sequence
    return list(
        tqdm(
            parallel_map(
                func=func,
                input_values=input_values,
                chunk_size=chunk_size,
                concurrency=concurrency,
            ),
            total=len(input_values),
            dynamic_ncols=True,
        )
    )
