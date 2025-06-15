import json
import os
import json
import urllib.request
from pathlib import Path
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import importlib
import types

run_pipeline = importlib.import_module("run_pipeline")

# Prepare dummy notion_hook_uploader before importing parse_failed_gpt
dummy_module = types.ModuleType("notion_hook_uploader")
def _dummy_parse(text: str):
    return {"dummy": text}
dummy_module.parse_generated_text = _dummy_parse
sys.modules["notion_hook_uploader"] = dummy_module

parse_failed_gpt = importlib.import_module("parse_failed_gpt")
notify_retry_result = importlib.import_module("notify_retry_result")


def test_parse_failed_creates_output(tmp_path: Path):
    input_file = tmp_path / "failed.json"
    output_file = tmp_path / "out.json"
    sample = [{"keyword": "test", "generated_text": "후킹문장1: a\n후킹문장2: b"}]
    input_file.write_text(json.dumps(sample, ensure_ascii=False))
    parse_failed_gpt.parse_failed(str(input_file), str(output_file))
    assert output_file.exists()
    data = json.loads(output_file.read_text())
    assert data[0]["keyword"] == "test"
    assert "parsed" in data[0]


def test_notify_retry_result_sends_message(monkeypatch, tmp_path: Path):
    summary = tmp_path / "summary.json"
    summary.write_text(json.dumps([{"keyword": "k", "retry_error": "x"}, {}], ensure_ascii=False))
    messages = []

    def fake_urlopen(req):
        messages.append(json.loads(req.data.decode("utf-8"))["text"])
        class Resp:
            status = 200
            def __enter__(self):
                return self
            def __exit__(self, exc_type, exc, tb):
                pass
        return Resp()

    monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)
    notify_retry_result.notify(str(summary), "http://example.com")
    assert messages and "Success: 1" in messages[0]


def test_run_pipeline_executes_all(monkeypatch, tmp_path: Path):
    scripts = []
    for i in range(3):
        path = tmp_path / f"s{i}.py"
        path.write_text("print('x')")
        scripts.append(str(path))

    monkeypatch.setattr(run_pipeline, "PIPELINE_SEQUENCE", scripts)
    run_pipeline.run_pipeline()
