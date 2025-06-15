import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.abspath("scripts"))

def _import_module():
    import importlib
    if "parse_failed_gpt" in sys.modules:
        return importlib.reload(sys.modules["parse_failed_gpt"])
    return importlib.import_module("parse_failed_gpt")

def test_parse_gpt_text():
    text = "h1\nh2\np1\np2\np3\nt1\nt2"
    mod = _import_module()
    parsed = mod.parse_gpt_text(text)
    assert parsed["hook_lines"] == ["h1", "h2"]
    assert parsed["blog_paragraphs"] == ["p1", "p2", "p3"]
    assert parsed["video_titles"] == ["t1", "t2"]

def test_parse_failed_gpt(tmp_path, monkeypatch):
    sample = [{"keyword": "k", "generated_text": "a\nb\nc\nd\ne\nf\ng"}]
    failed = tmp_path / "failed.json"
    output = tmp_path / "out.json"
    failed.write_text(json.dumps(sample, ensure_ascii=False))
    monkeypatch.setenv("FAILED_HOOK_PATH", str(failed))
    monkeypatch.setenv("REPARSED_OUTPUT_PATH", str(output))
    mod = _import_module()
    parsed = mod.parse_failed_gpt()
    assert parsed[0]["keyword"] == "k"
    assert output.exists()
    data = json.loads(output.read_text())
    assert data == parsed
