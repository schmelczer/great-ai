from typing import Any, Mapping, Optional, Type, TypeVar

import httpx
from pydantic import BaseModel

from ..errors.remote_call_error import RemoteCallError
from ..views import Trace

T = TypeVar("T", bound=BaseModel)


async def call_remote_great_ai_async(
    base_uri: str,
    data: Mapping[str, Any],
    retry_count: int = 4,
    timeout_in_seconds: Optional[int] = 300,
    model_class: Optional[Type[T]] = None,
) -> Trace[T]:

    if base_uri.endswith("/"):
        base_uri = base_uri[:-1]

    if not base_uri.endswith("/predict"):
        base_uri = f"{base_uri}/predict"

    transport = httpx.AsyncHTTPTransport(retries=retry_count)

    try:
        async with httpx.AsyncClient(
            transport=transport, timeout=timeout_in_seconds
        ) as client:
            response = await client.post(base_uri, json=data)
            try:
                response.raise_for_status()
            except Exception:
                raise RemoteCallError("Unexpected status code")
    except Exception as e:
        raise RemoteCallError from e

    try:
        trace = response.json()
    except Exception:
        raise RemoteCallError(
            f"JSON parsing failed {response.text}",
        )
    try:
        if model_class is not None:
            trace["output"] = model_class.parse_obj(trace["output"])
        return Trace.parse_obj(trace)
    except Exception:
        raise RemoteCallError("Could not parse Trace")
