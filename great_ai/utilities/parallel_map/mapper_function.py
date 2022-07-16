import asyncio
import inspect
import multiprocessing as mp
import queue
import threading
import traceback
from multiprocessing.synchronize import Event
from typing import Any, Awaitable, Callable, List, TypeVar, Union, cast

import dill

from .map_result import MapResult

T = TypeVar("T")
V = TypeVar("V")


def mapper_function(
    input_queue: Union[mp.Queue, queue.Queue],
    output_queue: Union[mp.Queue, queue.Queue],
    should_stop: Union[Event, threading.Event],
    func: Union[bytes, Callable[[T], V], Callable[[T], Awaitable[V]]],
) -> None:
    try:
        if isinstance(func, bytes):
            func = cast(Callable[[T], V], dill.loads(func))

        is_asynchronous = inspect.iscoroutinefunction(func)

        last_chunk: List[MapResult] = []
        while not should_stop.wait(0.1):
            if not last_chunk:
                try:
                    input_chunk = input_queue.get_nowait()
                    if is_asynchronous:

                        async def safe(i: int, value: T) -> Any:
                            try:
                                return MapResult(
                                    i,
                                    await cast(Callable[[T], Awaitable[V]], func)(
                                        value
                                    ),
                                )
                            except Exception as e:
                                # `e` has to be stringified in order to avoid any
                                # surprising serialization error when returning it
                                return MapResult(
                                    i, None, str(e), traceback.format_exc()
                                )

                        async def main() -> List[MapResult]:
                            return await asyncio.gather(
                                *[safe(i, v) for i, v in input_chunk]
                            )

                        last_chunk = asyncio.run(main())
                    else:
                        for i, value in input_chunk:
                            try:
                                last_chunk.append(MapResult(i, func(value)))
                            except Exception as e:
                                last_chunk.append(
                                    # `e` has to be stringified in order to avoid any
                                    # surprising serialization error when returning it
                                    MapResult(i, None, str(e), traceback.format_exc())
                                )
                except queue.Empty:
                    pass

            if last_chunk:
                try:
                    output_queue.put_nowait(last_chunk)
                    last_chunk = []
                except queue.Full:
                    pass
    except (KeyboardInterrupt, BrokenPipeError):
        pass
