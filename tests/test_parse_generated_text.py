import json
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from notion_hook_uploader import parse_generated_text

def test_parse_generated_text_json():
    sample = json.dumps({
        "hook_lines": ["Hook1", "Hook2"],
        "blog_paragraphs": ["Para1", "Para2", "Para3"],
        "video_titles": ["Title1", "Title2"]
    })
    result = parse_generated_text(sample)
    assert result["hook_lines"] == ["Hook1", "Hook2"]
    assert result["blog_paragraphs"] == ["Para1", "Para2", "Para3"]
    assert result["video_titles"] == ["Title1", "Title2"]
