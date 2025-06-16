import os
import sys
import types
import importlib

sys.modules['notion_client'] = types.SimpleNamespace(Client=lambda *a, **k: None)
sys.modules['dotenv'] = types.SimpleNamespace(load_dotenv=lambda: None)

os.makedirs('logs', exist_ok=True)

notion_hook_uploader = importlib.import_module('notion_hook_uploader')


def test_parse_generated_text_basic():
    text = (
        '후킹 문장1: first\n'
        '후킹 문장2: second\n'
        '블로그 초안: paragraph one\n'
        'paragraph two\n'
        'paragraph three\n'
        '영상 제목:\n'
        '- Title1\n'
        '- Title2\n'
    )
    result = notion_hook_uploader.parse_generated_text(text)
    assert result['hook_lines'] == ['first', 'second']
    assert result['blog_paragraphs'] == ['paragraph one']
    assert result['video_titles'] == ['Title2']


def test_parse_generated_text_empty():
    result = notion_hook_uploader.parse_generated_text('')
    assert result['hook_lines'] == ['', '']
    assert result['blog_paragraphs'] == ['', '', '']
    assert result['video_titles'] == ['', '']
