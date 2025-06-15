import asyncio
import time
import os
import json
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import keyword_auto_pipeline as kap
import pytest


@pytest.mark.asyncio
async def test_collect_data(monkeypatch):
    async def dummy_google(keyword, session):
        await asyncio.sleep(0.01)
        return {"keyword": keyword, "source": "GoogleTrends", "score": 80, "growth": 1.5, "cpc": 1500}

    async def dummy_twitter(keyword, session):
        await asyncio.sleep(0.01)
        return {"keyword": keyword, "source": "Twitter", "mentions": 50, "top_retweet": 100, "cpc": 1500}

    async with kap.aiohttp.ClientSession() as session:
        monkeypatch.setattr(kap, "fetch_google_trends", dummy_google)
        monkeypatch.setattr(kap, "fetch_twitter_metrics", dummy_twitter)
        results = await kap.collect_data_for_keyword("테스트", session)

    assert len(results) == 2
    assert results[0]["keyword"] == "테스트"


@pytest.mark.asyncio
async def test_pipeline_concurrency(monkeypatch, tmp_path):
    async def slow_google(keyword, session):
        await asyncio.sleep(0.1)
        return {"keyword": keyword, "source": "GoogleTrends", "score": 80, "growth": 1.5, "cpc": 1500}

    async def slow_twitter(keyword, session):
        await asyncio.sleep(0.1)
        return {"keyword": keyword, "source": "Twitter", "mentions": 50, "top_retweet": 100, "cpc": 1500}

    monkeypatch.setattr(kap, "fetch_google_trends", slow_google)
    monkeypatch.setattr(kap, "fetch_twitter_metrics", slow_twitter)
    monkeypatch.setattr(kap, "TOPIC_DETAILS", {"t": ["a", "b", "c", "d", "e"]})
    out = tmp_path / "out.json"
    monkeypatch.setenv("KEYWORD_OUTPUT_PATH", str(out))
    monkeypatch.setattr(kap, "OUTPUT_PATH", str(out))

    start = time.perf_counter()
    await kap.run_pipeline(concurrency=5)
    fast = time.perf_counter() - start

    start = time.perf_counter()
    await kap.run_pipeline(concurrency=1)
    slow = time.perf_counter() - start

    assert fast < slow
    data = json.loads(out.read_text())
    assert "filtered_keywords" in data
