import asyncio
from typing import Any, Mapping

from ...utilities import get_logger
from ..views import Trace
from .call_remote_great_ai_async import call_remote_great_ai_async

logger = get_logger("call_remote_great_ai")


def call_remote_great_ai(
    base_uri: str, data: Mapping[str, Any], retry_count: int = 4
) -> Trace:
    try:
        asyncio.get_running_loop()
        raise Exception(
            f"Already running in an event loop, you have to call `{call_remote_great_ai_async.__name__}`"
        )
    except RuntimeError:
        pass

    future = call_remote_great_ai_async(
        base_uri=base_uri, data=data, retry_count=retry_count
    )

    return asyncio.run(future)
