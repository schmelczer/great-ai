import asyncio
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
    timeout_in_seconds: Optional[float] = 300,
    model_class: Optional[Type[T]] = None,
) -> Trace[T]:
    """Communicate with a GreatAI object through an HTTP request.

    Send a POST request using [httpx](https://www.python-httpx.org/) to implement a
    remote call. Transport failures are retried up to `retry_count` times. A retry
    may repeat a prediction when its previous response was lost.

    The return value is inflated into a Trace. If `model_class` is specified, the
    original output is deserialised.

    Args:
        base_uri: Address of the remote instance, example: 'http://localhost:6060'
        data: The input sent as a json to the remote instance.
        retry_count: Retry on any HTTP communication failure.
        timeout_in_seconds: Overall permissible max length of the request. `None` means
            no timeout.
        model_class: A subtype of BaseModel to be used for deserialising the `.output`
            of the trace.
    """

    if base_uri.endswith("/"):
        base_uri = base_uri[:-1]

    if not base_uri.endswith("/predict"):
        base_uri = f"{base_uri}/predict"

    if retry_count < 0:
        raise ValueError("retry_count must be non-negative")
    transport = httpx.AsyncHTTPTransport(retries=0)

    try:
        async with (
            asyncio.timeout(timeout_in_seconds),
            httpx.AsyncClient(
                transport=transport, timeout=timeout_in_seconds
            ) as client,
        ):
            for attempt in range(retry_count + 1):
                try:
                    response = await client.post(base_uri, json=data)
                    break
                except httpx.TransportError:
                    if attempt == retry_count:
                        raise
                    await asyncio.sleep(min(0.1 * 2**attempt, 1))
            try:
                response.raise_for_status()
            except Exception:
                raise RemoteCallError(
                    f"Unexpected status code, reason: {response.text}"
                )
    except TimeoutError as e:
        raise RemoteCallError("Remote prediction exceeded its overall timeout") from e
    except Exception as e:
        raise RemoteCallError(str(e)) from e

    try:
        trace = response.json()
    except Exception:
        raise RemoteCallError(
            f"JSON parsing failed {response.text}",
        )
    try:
        if model_class is not None:
            trace["output"] = model_class.model_validate(trace["output"])
        return Trace.model_validate(trace)
    except Exception:
        raise RemoteCallError("Could not parse Trace")
