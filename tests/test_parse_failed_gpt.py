import json
import importlib
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def test_parse_failed_gpt(tmp_path, monkeypatch):
    failed_path = tmp_path / "failed.json"
    output_path = tmp_path / "reparsed.json"
    sample_text = (
        "후킹 문장1: a\n"
        "후킹 문장2: b\n"
        "블로그 초안:\n문단1\n문단2\n문단3\n"
        "영상 제목:\n- 제목1\n- 제목2\n"
    )
    with open(failed_path, "w", encoding="utf-8") as f:
        json.dump([{"keyword": "test", "generated_text": sample_text}], f, ensure_ascii=False)

    monkeypatch.setenv("FAILED_HOOK_PATH", str(failed_path))
    monkeypatch.setenv("REPARSED_OUTPUT_PATH", str(output_path))

    module = importlib.import_module("scripts.parse_failed_gpt")
    importlib.reload(module)
    module.parse_failed_gpt()

    with open(output_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert data[0]["parsed"]["hook_lines"] == ["a", "b"]
    assert data[0]["parsed"]["blog_paragraphs"][0] == "문단1"
    assert data[0]["parsed"]["video_titles"]
