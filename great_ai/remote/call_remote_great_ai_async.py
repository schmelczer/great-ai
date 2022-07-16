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
    """Communicate with a GreatAI object through an HTTP request.

    Send a POST request using [httpx](https://www.python-httpx.org/) to implement a
    remote call. Error-handling and retries are provided by httpx.

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

    transport = httpx.AsyncHTTPTransport(retries=retry_count)

    try:
        async with httpx.AsyncClient(
            transport=transport, timeout=timeout_in_seconds
        ) as client:
            response = await client.post(base_uri, json=data)
            try:
                response.raise_for_status()
            except Exception:
                raise RemoteCallError(
                    f"Unexpected status code, reason: {response.text}"
                )
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
