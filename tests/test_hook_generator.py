import asyncio
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import importlib
import openai
import pytest

class DummyResponse:
    def __init__(self, content: str):
        self.choices = [type("c", (), {"message": {"content": content}})]

@pytest.mark.usefixtures("monkeypatch")
def test_generate_hooks_async(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    data = {
        "filtered_keywords": [
            {"keyword": "testkw", "source": "src", "score": 1, "growth": 1, "mentions": 1}
        ]
    }
    keywords_path = tmp_path / "keywords.json"
    keywords_path.write_text(json.dumps(data), encoding="utf-8")

    out_path = tmp_path / "out.json"
    fail_path = tmp_path / "fail.json"

    monkeypatch.setenv("KEYWORD_OUTPUT_PATH", str(keywords_path))
    monkeypatch.setenv("HOOK_OUTPUT_PATH", str(out_path))
    monkeypatch.setenv("FAILED_HOOK_PATH", str(fail_path))
    monkeypatch.setenv("OPENAI_API_KEY", "test")
    monkeypatch.setenv("API_DELAY", "0")

    import hook_generator
    importlib.reload(hook_generator)

    async def fake_acreate(**_: object) -> DummyResponse:
        return DummyResponse("l1\nl2\nl3\nl4\nl5\nl6")

    monkeypatch.setattr(openai.ChatCompletion, "acreate", fake_acreate)

    asyncio.run(hook_generator.generate_hooks())

    output = json.loads(out_path.read_text(encoding="utf-8"))
    assert output[0]["keyword"] == "testkw"
    assert output[0]["hook_lines"] == ["l1", "l2"]
