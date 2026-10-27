import asyncio
import json
from typing import Any, AsyncIterator
from unittest.mock import patch

import httpx
import pytest
from great_ai import RemoteCallError, call_remote_great_ai_async


def response_trace() -> Any:
    return dict(
        trace_id="remote",
        created="2026-01-01",
        original_execution_time_ms=0,
        models=[],
        tags=[],
        logged_values={},
        output=7,
    )


@pytest.mark.asyncio
async def test_remote_call_retries_response_read_failures() -> None:
    calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        if calls == 1:
            raise httpx.ReadError("response disconnected")
        return httpx.Response(200, json=response_trace())

    with patch(
        "great_ai.remote.call_remote_great_ai_async.httpx.AsyncHTTPTransport",
        return_value=httpx.MockTransport(handler),
    ):
        assert (
            await call_remote_great_ai_async("http://test", {}, retry_count=2)
        ).output == 7
    assert calls == 2


@pytest.mark.asyncio
async def test_overall_timeout_limits_slow_streaming_responses() -> None:
    class SlowStream(httpx.AsyncByteStream):
        async def __aiter__(self) -> AsyncIterator[bytes]:
            payload = json.dumps(response_trace()).encode()
            for offset in range(0, len(payload), 10):
                await asyncio.sleep(0.01)
                yield payload[offset : offset + 10]

    transport = httpx.MockTransport(
        lambda request: httpx.Response(200, stream=SlowStream())
    )
    with patch(
        "great_ai.remote.call_remote_great_ai_async.httpx.AsyncHTTPTransport",
        return_value=transport,
    ):
        with pytest.raises(RemoteCallError, match="overall timeout") as error:
            await call_remote_great_ai_async(
                "http://test", {}, timeout_in_seconds=0.025
            )
    assert isinstance(error.value.__cause__, TimeoutError)


@pytest.mark.asyncio
async def test_remote_retry_limit_is_respected() -> None:
    calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        raise httpx.ReadError("response disconnected")

    with patch(
        "great_ai.remote.call_remote_great_ai_async.httpx.AsyncHTTPTransport",
        return_value=httpx.MockTransport(handler),
    ):
        with pytest.raises(RemoteCallError, match="response disconnected"):
            await call_remote_great_ai_async("http://test", {}, retry_count=1)
    assert calls == 2
