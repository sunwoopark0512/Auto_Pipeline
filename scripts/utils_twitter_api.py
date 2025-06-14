"""Async Twitter API v2 helper with session reuse and jittered retries."""

from __future__ import annotations

import json
import os
import time
from typing import Any, Dict, List, TypedDict

import aiohttp
from aiolimiter import AsyncLimiter
from tenacity import retry, stop_after_attempt, wait_random_exponential

BEARER = os.getenv("TWITTER_BEARER_TOKEN", "")
HEADERS = {"Authorization": f"Bearer {BEARER}"}

_RATE_LIMITER_SEC = AsyncLimiter(25, 1)
_RATE_LIMITER_MIN = AsyncLimiter(1000, 60)
_SEARCH_URL = "https://api.twitter.com/2/tweets/search/recent"
_SESSION: aiohttp.ClientSession | None = None


class TweetPayload(TypedDict):
    """Simplified tweet payload."""

    id: str
    text: str
    created_at: str
    public_metrics: Dict[str, Any]


async def _get_session() -> aiohttp.ClientSession:
    global _SESSION
    if _SESSION is None or _SESSION.closed:
        _SESSION = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=20))
    return _SESSION


async def close_session() -> None:
    """Close the global session."""

    global _SESSION
    if _SESSION and not _SESSION.closed:
        await _SESSION.close()
    _SESSION = None


class TwitterAPI:
    """Context-managed access to Twitter API v2."""

    async def __aenter__(self) -> "TwitterAPI":
        await _get_session()
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await close_session()

    @retry(
        wait=wait_random_exponential(multiplier=1, max=60), stop=stop_after_attempt(5), reraise=True
    )
    async def search_recent(self, query: str, max_results: int = 25) -> List[TweetPayload]:
        """Return recent tweets for the query."""

        params = {
            "query": query,
            "max_results": str(max_results),
            "tweet.fields": "public_metrics,created_at",
        }

        async with _RATE_LIMITER_SEC:
            async with _RATE_LIMITER_MIN:
                session = await _get_session()
                t0 = time.perf_counter()
                async with session.get(_SEARCH_URL, headers=HEADERS, params=params) as resp:
                    latency = round((time.perf_counter() - t0) * 1000, 2)
                    if resp.status != 200:
                        body = await resp.text()
                        print(json.dumps({"metric": "twitter.api.error", "value": 1}))
                        raise RuntimeError(f"Twitter API {resp.status}: {body}")
                    data = await resp.json()
                    count = len(data.get("data", []))
                    print(json.dumps({"metric": "twitter.api.latency", "value": latency}))
                    print(json.dumps({"metric": "twitter.api.count", "value": count}))
                    return data.get("data", [])
