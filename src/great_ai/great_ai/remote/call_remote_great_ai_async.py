from typing import Any, Mapping, Optional

from ..views import Trace
from .http_client import HttpClient
from .remote_call_error import RemoteCallError

http: Optional[HttpClient] = None


async def call_remote_great_ai_async(
    base_uri: str, data: Mapping[str, Any], retry_count: int = 4
) -> Trace:
    global http
    if http is None:
        http = HttpClient()

    url = f"{base_uri}/predict/"
    response = await http.post(
        url=url, data=data, retry_count=retry_count, expected_status=200
    )

    try:
        return Trace.parse_obj(response)
    except Exception:
        raise RemoteCallError("Could not parse response")
