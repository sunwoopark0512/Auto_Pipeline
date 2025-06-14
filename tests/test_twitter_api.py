"""Tests for Twitter API helper."""

import aiohttp
import pytest

from scripts.utils_twitter_api import TwitterAPI


@pytest.mark.asyncio
async def test_search_recent_invalid_token(monkeypatch):
    """search_recent should raise RuntimeError on non-200 responses."""

    class FakeResp:
        status = 401

        async def text(self):
            return "unauthorized"

        async def json(self):
            return {}

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            return False

    def fake_get(*args, **kwargs):
        return FakeResp()

    monkeypatch.setattr(aiohttp.ClientSession, "get", fake_get)
    async with TwitterAPI() as api:
        with pytest.raises(RuntimeError):
            await api.search_recent("#pytest", 10)
