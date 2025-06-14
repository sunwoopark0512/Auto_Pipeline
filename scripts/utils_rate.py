"""Async rate limiting utilities with retry support."""

from __future__ import annotations

import asyncio
import logging
from types import TracebackType
from typing import Any, Awaitable, Callable, TypeVar

from aiolimiter import AsyncLimiter
from tenacity import (RetryCallState, retry, retry_if_exception_type,
                      stop_after_attempt, wait_exponential, wait_random)


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
        # aiolimiter does not expose a release method; tokens recover over time.
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


def notion_rate_limited(
    func: Callable[..., Awaitable[T]],
) -> Callable[..., Awaitable[T]]:
    """Wrap a coroutine with Notion-specific rate limits and retries."""

    @retry(
        wait=wait_exponential(multiplier=1, min=2, max=10) + wait_random(0, 1),
        stop=stop_after_attempt(3),
        after=_after_retry,
    )
    async def wrapper(
        *args: Any, **kwargs: Any
    ) -> T:  # pylint: disable=missing-function-docstring
        # type: ignore[override]
        async with NOTION_LIMITER:
            return await func(*args, **kwargs)

    return wrapper


# ---------- Twitter RateLimiter ----------
TWITTER_LIMITER = CombinedLimiter(
    AsyncLimiter(5, 1),
    AsyncLimiter(250, 60),
    AsyncLimiter(50, 15),
)


def _maybe_retry_after(exc: BaseException) -> float:
    """Return delay from Retry-After header when available."""
    resp = getattr(exc, "response", None)
    if resp is not None and getattr(resp, "status", None) == 429:
        try:
            return float(resp.headers.get("Retry-After", 0))
        except (ValueError, TypeError, AttributeError):
            return 0
    return 0


def twitter_rate_limited(
    func: Callable[..., Awaitable[T]],
) -> Callable[..., Awaitable[T]]:
    """Twitter 스크레이퍼 전용 데코레이터."""

    @retry(
        wait=wait_exponential(multiplier=1, min=2, max=10) + wait_random(0, 1),
        stop=stop_after_attempt(4),
        retry=retry_if_exception_type(Exception),
        after=_after_retry,
    )
    async def wrapper(
        *args: Any, **kwargs: Any
    ) -> T:  # pylint: disable=missing-function-docstring
        # type: ignore[override]
        async with TWITTER_LIMITER:
            try:
                return await func(*args, **kwargs)
            except Exception as exc:  # pylint: disable=broad-except
                delay = _maybe_retry_after(exc)
                if delay:
                    await asyncio.sleep(delay)
                raise

    return wrapper
