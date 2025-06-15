"""Async OpenAI helper functions.

Usage::

    from scripts.ai_async import batch_generate
    import asyncio, os

    prompts = ["Give me a viral hook about AI", ...]
    hooks = asyncio.run(batch_generate(prompts))
"""

from __future__ import annotations

import asyncio
import os
import logging
from typing import Sequence, List

try:
    from openai import AsyncOpenAI
except ImportError:  # pragma: no cover
    AsyncOpenAI = None  # type: ignore

from tenacity import retry, stop_after_attempt, wait_random_exponential
from aiolimiter import AsyncLimiter

_logger = logging.getLogger(__name__)

# OpenAI rate-limit: 3K TPM & 200 RPM on GPT-4o (example) → 3 req/sec conservative
_limiter = AsyncLimiter(max_rate=3, time_period=1.0)

_client: AsyncOpenAI | None = None


def _get_client() -> AsyncOpenAI:
    global _client
    if _client is None:
        if AsyncOpenAI is None:  # pragma: no cover
            raise RuntimeError("openai package with async support is required")
        _client = AsyncOpenAI()
    return _client


@retry(stop=stop_after_attempt(5), wait=wait_random_exponential(multiplier=2, max=30))
async def _call_openai(prompt: str) -> str:
    """Single chat completion with retry & limiter."""

    async with _limiter:
        client = _get_client()
        resp = await client.chat.completions.create(
            model="gpt-4o-mini",  # configurable via env if needed
            messages=[{"role": "user", "content": prompt}],
        )
        content = resp.choices[0].message.content or ""
        usage = resp.usage
        _logger.info(
            "openai_request_tokens=%s openai_response_tokens=%s",
            usage.prompt_tokens,
            usage.completion_tokens,
        )
        return content


async def batch_generate(prompts: Sequence[str], concurrency: int = 5) -> List[str]:
    """Generate completions for multiple prompts concurrently."""

    if os.getenv("DRY_RUN"):
        _logger.warning("DRY_RUN=1 → returning placeholder hooks")
        return [f"[DRY] {p[:20]}…" for p in prompts]

    sem = asyncio.Semaphore(concurrency)

    async def _task(prompt: str) -> str:
        async with sem:
            return await _call_openai(prompt)

    return await asyncio.gather(*[_task(p) for p in prompts])
