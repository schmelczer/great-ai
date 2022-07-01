import asyncio
from typing import Any, Mapping, Optional, Type, TypeVar

from pydantic import BaseModel

from ...utilities import get_logger
from ..views import Trace
from .call_remote_great_ai_async import call_remote_great_ai_async

logger = get_logger("call_remote_great_ai")

T = TypeVar("T", bound=BaseModel)


def call_remote_great_ai(
    base_uri: str,
    data: Mapping[str, Any],
    retry_count: int = 4,
    model_class: Optional[Type[T]] = None,
) -> Trace[T]:
    try:
        asyncio.get_running_loop()
        raise Exception(
            f"Already running in an event loop, you have to call `{call_remote_great_ai_async.__name__}`"
        )
    except RuntimeError:
        pass

    future = call_remote_great_ai_async(
        base_uri=base_uri, data=data, retry_count=retry_count, model_class=model_class
    )

    return asyncio.run(future)
