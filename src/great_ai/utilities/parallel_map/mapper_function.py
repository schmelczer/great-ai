import multiprocessing as mp
import queue
import threading
import traceback
from time import sleep
from typing import Callable, Union

import dill


def mapper_function(
    input_queue: Union[mp.Queue, queue.Queue],
    output_queue: Union[mp.Queue, queue.Queue],
    should_stop: Union[mp.Event, threading.Event],
    map_function: Union[bytes, Callable],
) -> None:
    try:
        if isinstance(map_function, bytes):
            map_function = dill.loads(map_function)

        last_chunk = None
        while not should_stop.is_set():
            if last_chunk is None:
                try:
                    input_chunk = input_queue.get_nowait()
                    last_chunk = []
                    for i, v in input_chunk:
                        result, exception = None, None
                        try:
                            result = map_function(v)
                        except Exception as e:
                            exception = e, traceback.format_exc()
                        last_chunk.append((i, result, exception))
                except queue.Empty:
                    sleep(
                        0.1
                    )  # input_queue.get(0.1) would hang in some cases with multiprocessing
            else:
                try:
                    output_queue.put_nowait(last_chunk)
                    last_chunk = None
                except queue.Full:
                    sleep(
                        0.1
                    )  # output_queue.put(0.1) would hang in some cases with multiprocessing
    except (KeyboardInterrupt, BrokenPipeError):
        pass
