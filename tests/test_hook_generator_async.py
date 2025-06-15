import json
import asyncio
from pathlib import Path
from unittest.mock import AsyncMock, patch

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest

@pytest.mark.asyncio
async def test_generate_hooks(tmp_path, monkeypatch):
    keywords_path = tmp_path / "keywords.json"
    output_path = tmp_path / "hooks.json"
    fail_path = tmp_path / "failed.json"

    data = {"filtered_keywords": [{"keyword": "test", "source": "s", "score": 1, "growth": 1, "mentions": 1}]}
    keywords_path.write_text(json.dumps(data), encoding="utf-8")

    monkeypatch.setenv("KEYWORD_OUTPUT_PATH", str(keywords_path))
    monkeypatch.setenv("HOOK_OUTPUT_PATH", str(output_path))
    monkeypatch.setenv("FAILED_HOOK_PATH", str(fail_path))
    monkeypatch.setenv("OPENAI_API_KEY", "sk")
    monkeypatch.setenv("API_DELAY", "0")

    import importlib
    hg = importlib.reload(__import__("hook_generator"))

    class _Resp:
        def __init__(self, content: str):
            self.choices = [type("Obj", (), {"message": {"content": content}})()]

    async_mock = AsyncMock(return_value=_Resp("a\nb\nc\nd\ne\nf"))

    with patch.object(hg.openai.ChatCompletion, "acreate", async_mock):
        await hg.generate_hooks()

    saved = json.loads(output_path.read_text(encoding="utf-8"))
    assert saved[0]["keyword"] == "test"
    assert "generated_text" in saved[0]

