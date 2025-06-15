import json
import sys
import os
import pytest

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import types
sys.modules['notion_client'] = types.SimpleNamespace(Client=lambda *a, **kw: None)
sys.modules['dotenv'] = types.SimpleNamespace(load_dotenv=lambda: None)
from notion_hook_uploader import parse_generated_text

def test_parse_valid_json():
    data = {
        "hook_lines": ["hook1", "hook2"],
        "blog_paragraphs": ["p1", "p2", "p3"],
        "video_titles": ["v1", "v2"]
    }
    text = json.dumps(data)
    parsed = parse_generated_text(text)
    assert parsed["hook_lines"] == ["hook1", "hook2"]
    assert parsed["blog_paragraphs"] == ["p1", "p2", "p3"]
    assert parsed["video_titles"] == ["v1", "v2"]

def test_parse_invalid_json():
    text = "not a json"
    parsed = parse_generated_text(text)
    assert parsed == {
        "hook_lines": ["", ""],
        "blog_paragraphs": ["", "", ""],
        "video_titles": ["", ""]
    }

def test_parse_missing_fields():
    data = {"hook_lines": ["h1"]}
    text = json.dumps(data)
    parsed = parse_generated_text(text)
    assert parsed == {
        "hook_lines": ["", ""],
        "blog_paragraphs": ["", "", ""],
        "video_titles": ["", ""]
    }
