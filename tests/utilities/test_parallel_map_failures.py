import os
import signal
import subprocess
import sys
import textwrap
from pathlib import Path

import pytest


@pytest.mark.parametrize("operation", ["close", "interrupt"])
def test_worker_failure_and_cancellation_finish(tmp_path: Path, operation: str) -> None:
    script = textwrap.dedent("""
        import multiprocessing as mp
        import os
        import time
        from great_ai.utilities import WorkerException, parallel_map

        def main(operation):
            if operation.startswith("dead_worker"):
                code = 0 if operation.endswith("zero") else 3
                try:
                    list(parallel_map(lambda _: os._exit(code), range(100), concurrency=1, chunk_size=1))
                except WorkerException as error:
                    assert f"exit code {code}" in str(error)
                else:
                    raise AssertionError("Unexpected worker exit was ignored")
            else:
                iterator = parallel_map(lambda x: 0 if x == 0 else time.sleep(60),
                                        range(100), concurrency=1, chunk_size=1)
                assert next(iterator) == 0
                if operation == "close":
                    iterator.close()
                else:
                    try:
                        iterator.throw(KeyboardInterrupt)
                    except KeyboardInterrupt:
                        pass
            assert not mp.active_children(), mp.active_children()

        if __name__ == "__main__":
            main(OPERATION)
    """).replace("OPERATION", repr(operation))
    process = subprocess.Popen(
        [sys.executable, "-c", script],
        cwd=tmp_path,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        start_new_session=os.name != "nt",
    )
    try:
        stdout, stderr = process.communicate(timeout=15)
    except subprocess.TimeoutExpired:
        if os.name == "nt":
            subprocess.run(
                ["taskkill", "/F", "/T", "/PID", str(process.pid)], capture_output=True
            )
        else:
            os.killpg(process.pid, signal.SIGKILL)
        stdout, stderr = process.communicate()
        pytest.fail(f"Parallel mapping did not finish: {stdout}\n{stderr}")
    assert process.returncode == 0, f"{stdout}\n{stderr}"
