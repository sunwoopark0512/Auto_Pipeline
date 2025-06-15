"""Unit tests for qa_filter module."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from qa_filter import load_banned_words, qa_filter  # noqa:E402

def test_qa_filter_basic(tmp_path):
    items = [
        {"keyword": "test", "generated_text": "good text", "hook_lines": ["hello"], "blog_paragraphs": ["para"], "video_titles": ["title"]},
        {"keyword": "bad", "generated_text": "금칙어1 포함", "hook_lines": ["bad"], "blog_paragraphs": ["para"], "video_titles": ["title"]},
        {"keyword": "empty", "generated_text": "", "hook_lines": [], "blog_paragraphs": [], "video_titles": []},
    ]
    banned_file = tmp_path / "banned.txt"
    banned_file.write_text("금칙어1\n")
    banned = load_banned_words(str(banned_file))
    passed, flagged = qa_filter(items, banned)
    assert len(passed) == 1
    assert len(flagged) == 2
    assert flagged[0]["qa_issue"] == "banned_word"
    assert flagged[1]["qa_issue"] == "empty_content"
