"""Async Twitter API v2 helper with rate limiting and retry."""

from __future__ import annotations

import json
import os
import time
from typing import Any, Dict, List

import aiohttp
from aiolimiter import AsyncLimiter
from tenacity import retry, stop_after_attempt, wait_exponential

BEARER = os.getenv("TWITTER_BEARER_TOKEN", "")
HEADERS = {"Authorization": f"Bearer {BEARER}"}

# Allow 25 requests per second and 1000 per minute
_RATE_LIMITER_SEC = AsyncLimiter(25, 1)
_RATE_LIMITER_MIN = AsyncLimiter(1000, 60)
_SEARCH_URL = "https://api.twitter.com/2/tweets/search/recent"


@retry(wait=wait_exponential(multiplier=1, min=2, max=30), stop=stop_after_attempt(5))
async def search_recent(
    session: aiohttp.ClientSession, query: str, max_results: int = 25
) -> List[Dict[str, Any]]:
    """Return recent tweet objects as JSON list."""
    params = {
        "query": query,
        "max_results": str(max_results),
        "tweet.fields": "public_metrics,created_at",
    }

    async with _RATE_LIMITER_SEC:
        async with _RATE_LIMITER_MIN:
            t0 = time.perf_counter()
            try:
                async with session.get(
                    _SEARCH_URL, headers=HEADERS, params=params, timeout=20
                ) as resp:
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
            except aiohttp.ClientError as exc:
                raise RuntimeError(str(exc)) from exc
