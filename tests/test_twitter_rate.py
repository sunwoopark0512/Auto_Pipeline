"""Tests for Twitter rate limiter utilities."""

import asyncio
import sys
import time
from pathlib import Path
from typing import Any, Coroutine, cast

import pytest
from tenacity import RetryError

sys.path.insert(
    0, str(Path(__file__).resolve().parents[1])
)  # pylint: disable=wrong-import-position

from scripts.utils_rate import (  # pylint: disable=wrong-import-position
    TWITTER_LIMITER, twitter_rate_limited)


async def dummy_twitter_call() -> None:
    """Acquire the limiter once."""
    async with TWITTER_LIMITER:
        return


def test_twitter_rate_limiter() -> None:
    """Ensure rate limiter throttles bursts."""

    async def _run() -> float:
        start = time.perf_counter()
        await asyncio.gather(*(dummy_twitter_call() for _ in range(20)))
        return time.perf_counter() - start

    duration = asyncio.run(_run())
    assert duration >= 3


class DummyHTTPError(Exception):
    """Simulate httpx.HTTPStatusError with Retry-After header."""

    def __init__(self, retry_after: int) -> None:
        self.response = type(
            "Resp",
            (),
            {"status": 429, "headers": {"Retry-After": str(retry_after)}},
        )


def test_retry_after_respected() -> None:
    """Wrapper should sleep based on Retry-After header."""
    calls: list[int] = []

    async def failing() -> None:
        """Always raise HTTP 429."""
        calls.append(1)
        raise DummyHTTPError(1)

    wrapped = twitter_rate_limited(failing)

    start = time.perf_counter()
    coro = wrapped()
    with pytest.raises(RetryError):
        asyncio.run(cast(Coroutine[Any, Any, None], coro))
    duration = time.perf_counter() - start
    assert len(calls) == 4
    assert duration >= 1
