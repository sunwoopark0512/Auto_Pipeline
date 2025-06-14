import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.utils_rate import TWITTER_LIMITER


async def dummy_twitter_call() -> None:
    async with TWITTER_LIMITER:
        return


def test_twitter_rate_limiter() -> None:
    """동시 20 호출해도 초당 5개 이하 제한."""

    async def _run() -> float:
        import time

        start = time.perf_counter()
        await asyncio.gather(*(dummy_twitter_call() for _ in range(20)))
        return time.perf_counter() - start

    duration = asyncio.run(_run())
    assert duration >= 3
