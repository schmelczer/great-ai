import multiprocessing as mp
import queue

import dill


def mapper_function(
    input_queue: mp.Queue,
    output_queue: mp.Queue,
    should_stop: mp.Event,
    serialized_map_function: bytes,
):
    map_function = dill.loads(serialized_map_function)
    try:
        while not should_stop.is_set():
            try:
                input_chunk = input_queue.get_nowait()
                output_chunk = [(i, map_function(v)) for i, v in input_chunk]
                output_queue.put(output_chunk)
            except queue.Empty:
                pass
    except KeyboardInterrupt:
        return
