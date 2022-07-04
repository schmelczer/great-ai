from typing import Any, Mapping, Optional, Type, TypeVar

from pydantic import BaseModel

from ..views import Trace
from .http_client import HttpClient
from .remote_call_error import RemoteCallError

http: Optional[HttpClient] = None

T = TypeVar("T", bound=BaseModel)


async def call_remote_great_ai_async(
    base_uri: str,
    data: Mapping[str, Any],
    retry_count: int = 4,
    model_class: Optional[Type[T]] = None,
) -> Trace[T]:
    global http
    if http is None:
        http = HttpClient()

    if base_uri.endswith("/"):
        base_uri = base_uri[:-1]

    url = f"{base_uri}/predict/"
    response = await http.post(
        url=url, data=data, retry_count=retry_count, expected_status=200
    )

    try:
        if model_class is not None:
            response["output"] = model_class.parse_obj(response["output"])
        return Trace.parse_obj(response)
    except Exception:
        raise RemoteCallError("Could not parse response")
