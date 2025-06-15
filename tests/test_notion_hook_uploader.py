import importlib
from unittest import mock


def test_parse_generated_text(monkeypatch):
    monkeypatch.setattr('logging.FileHandler', lambda *a, **k: mock.Mock())
    module = importlib.import_module('notion_hook_uploader')
    sample = (
        "후킹 문장1: Hook1\n"
        "후킹문장2: Hook2\n"
        "블로그 초안:\n"
        "Para1\n"
        "Para2\n"
        "Para3\n"
        "영상 제목:\n"
        "- Title1\n"
        "- Title2\n"
    )
    parsed = module.parse_generated_text(sample)
    assert parsed["hook_lines"] == ["Hook1", "Hook2"]
    assert parsed["blog_paragraphs"] == ["Para1"]
    assert parsed["video_titles"] == ["Title2"]
