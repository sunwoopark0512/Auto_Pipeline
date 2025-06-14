from __future__ import annotations

import logging
from typing import Any, Awaitable, Callable, TypeVar

from aiolimiter import AsyncLimiter
from tenacity import RetryCallState, retry, stop_after_attempt, wait_exponential
from types import TracebackType


class CombinedLimiter:
    """Combine multiple AsyncLimiters into one context manager."""

    def __init__(self, *limiters: AsyncLimiter) -> None:
        self.limiters = limiters

    async def __aenter__(self) -> "CombinedLimiter":
        for limiter in self.limiters:
            await limiter.acquire()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        return None


T = TypeVar("T")


# ---------------------- Retry Helper ----------------------

def _after_retry(retry_state: RetryCallState) -> None:
    if retry_state.outcome is not None:  # type: ignore[truthy-bool]
        err = retry_state.outcome.exception()  # type: ignore[union-attr]
    else:
        err = None
    logging.warning("retry", extra={"error": str(err)})


# ---------- Notion RateLimiter ----------
NOTION_LIMITER = CombinedLimiter(AsyncLimiter(3, 1), AsyncLimiter(60, 60))


def notion_rate_limited(func: Callable[..., Awaitable[T]]) -> Callable[..., Awaitable[T]]:
    @retry(wait=wait_exponential(multiplier=1, min=2, max=10), stop=stop_after_attempt(3), after=_after_retry)
    async def wrapper(*args: Any, **kwargs: Any) -> T:  # type: ignore[override]
        async with NOTION_LIMITER:
            return await func(*args, **kwargs)

    return wrapper


# ---------- Twitter RateLimiter ----------
TWITTER_LIMITER = CombinedLimiter(
    AsyncLimiter(5, 1),
    AsyncLimiter(250, 60),
    AsyncLimiter(50, 15),
)


def twitter_rate_limited(func: Callable[..., Awaitable[T]]) -> Callable[..., Awaitable[T]]:
    """Twitter 스크레이퍼 전용 데코레이터."""

    @retry(wait=wait_exponential(multiplier=1, min=2, max=10), stop=stop_after_attempt(4), after=_after_retry)
    async def wrapper(*args: Any, **kwargs: Any) -> T:  # type: ignore[override]
        async with TWITTER_LIMITER:
            return await func(*args, **kwargs)

    return wrapper


