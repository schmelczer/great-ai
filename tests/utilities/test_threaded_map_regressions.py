import subprocess
import sys
import threading
from typing import Generator, cast

import pytest
from great_ai.utilities import WorkerException, threaded_parallel_map


@pytest.mark.parametrize("exception", ["SystemExit", "KeyboardInterrupt"])
def test_exited_thread_is_reported(exception: str) -> None:
    script = f"""
from great_ai.utilities import threaded_parallel_map, WorkerException
def dead(value):
    raise {exception}()
try:
    list(threaded_parallel_map(dead, [1], concurrency=1))
except WorkerException as error:
    assert 'exited unexpectedly' in str(error)
else:
    raise AssertionError('Worker exit was ignored')
"""
    result = subprocess.run(
        [sys.executable, "-c", script], capture_output=True, text=True, timeout=10
    )
    assert result.returncode == 0, result.stderr


@pytest.mark.parametrize("fail", [False, True])
def test_thread_workers_stop_after_close_or_error(fail: bool) -> None:
    def predict(value: int) -> int:
        if fail:
            raise ValueError("failed")
        return value

    before = set(threading.enumerate())
    iterator = cast(
        Generator[int, None, None],
        threaded_parallel_map(predict, range(100), concurrency=2, chunk_size=1),
    )
    if fail:
        with pytest.raises(WorkerException):
            next(iterator)
    else:
        assert next(iterator) == 0
        iterator.close()
    assert not set(threading.enumerate()) - before
