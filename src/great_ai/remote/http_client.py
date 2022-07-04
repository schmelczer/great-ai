import logging
from asyncio import sleep
from typing import Any, Mapping, Optional

import aiohttp

from .remote_call_error import RemoteCallError

logger = logging.getLogger("http")


class HttpClient:
    timeout_seconds: int = 600
    wait_between_retries_seconds: float = 5

    def __init__(
        self,
    ) -> None:
        timeout = aiohttp.ClientTimeout(total=self.timeout_seconds)

        self._session = aiohttp.ClientSession(
            raise_for_status=False,
            timeout=timeout,
        )

    async def post(
        self,
        url: str,
        data: Mapping[str, Any],
        retry_count: int = 0,
        expected_status: Optional[int] = None,
        **kwargs: Any,
    ) -> Any:
        for i in range(retry_count + 1):
            try:
                async with self._session.post(url, json=data, **kwargs) as r:
                    if (
                        expected_status is not None and r.status != expected_status
                    ) or r.status >= 500:
                        response_text = await r.text()
                        raise ValueError(
                            f"Found not-expected status code: {r.status}, response is: {response_text}"
                        )
                    try:
                        return await r.json()
                    except Exception:
                        raise RemoteCallError(
                            "JSON parsing failed",
                        )
            except Exception as e:
                if retry_count - i > 1:
                    logger.warning(
                        f"Request failed ({e}), {retry_count - i - 1} retries left",
                    )
                    await sleep(self.wait_between_retries_seconds)

        raise RemoteCallError(f"Request has failed too many ({retry_count + 1}) times")

    async def close(self) -> None:
        await self._session.close()
