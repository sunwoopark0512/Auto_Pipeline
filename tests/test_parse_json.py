import json
import os
import sys
import types
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
class DummyClient:
    def __init__(self, *_, **__):
        pass

sys.modules['notion_client'] = types.SimpleNamespace(Client=DummyClient)
sys.modules['dotenv'] = types.SimpleNamespace(load_dotenv=lambda: None)
logging.FileHandler = lambda *args, **kwargs: logging.NullHandler()
from notion_hook_uploader import parse_generated_text

def test_parse_valid_json():
    text = json.dumps({
        "hook_lines": ["h1", "h2"],
        "blog_paragraphs": ["p1", "p2", "p3"],
        "video_titles": ["v1", "v2"]
    })
    parsed = parse_generated_text(text)
    assert parsed["hook_lines"] == ["h1", "h2"]
    assert parsed["blog_paragraphs"] == ["p1", "p2", "p3"]
    assert parsed["video_titles"] == ["v1", "v2"]

def test_parse_invalid_json():
    parsed = parse_generated_text("not json")
    assert parsed["hook_lines"] == ["", ""]
    assert parsed["blog_paragraphs"] == ["", "", ""]
    assert parsed["video_titles"] == ["", ""]
