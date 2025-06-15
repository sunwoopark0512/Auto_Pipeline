import asyncio
import os
import sys
from types import SimpleNamespace

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts import ai_async


@pytest.mark.asyncio
async def test_batch_generate_dry_run(monkeypatch):
    monkeypatch.setenv("DRY_RUN", "1")
    res = await ai_async.batch_generate(["hello", "world"])
    assert res == ["[DRY] hello…", "[DRY] world…"]
    monkeypatch.delenv("DRY_RUN")


@pytest.mark.asyncio
async def test_batch_generate_concurrency(monkeypatch):
    calls = []
    concurrent = 0
    max_concurrent = 0
    lock = asyncio.Lock()

    class DummyResp:
        def __init__(self, text):
            self.choices = [SimpleNamespace(message=SimpleNamespace(content=text))]
            self.usage = SimpleNamespace(prompt_tokens=1, completion_tokens=1)

    class DummyAsyncOpenAI:
        def __init__(self):
            self.chat = self
            self.completions = self

        async def create(self, model, messages):
            nonlocal concurrent, max_concurrent
            async with lock:
                concurrent += 1
                max_concurrent = max(max_concurrent, concurrent)
            await asyncio.sleep(0.01)
            async with lock:
                concurrent -= 1
            calls.append(messages[0]["content"])
            return DummyResp(messages[0]["content"] + "_resp")

    monkeypatch.setattr(ai_async, "AsyncOpenAI", DummyAsyncOpenAI)
    ai_async._client = None
    prompts = ["a", "b", "c", "d"]
    res = await ai_async.batch_generate(prompts, concurrency=2)
    assert res == [p + "_resp" for p in prompts]
    assert max_concurrent <= 2
    assert calls == prompts
