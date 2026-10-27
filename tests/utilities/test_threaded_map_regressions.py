import subprocess
import sys

import pytest


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
