import os
import sys
import types
import importlib

# create required directories and dummy modules before import
os.makedirs('logs', exist_ok=True)
sys.modules['dotenv'] = types.SimpleNamespace(load_dotenv=lambda: None)
sys.modules['notion_client'] = types.SimpleNamespace(Client=lambda *a, **k: None)

nhu = importlib.import_module('notion_hook_uploader')


def test_parse_generated_text():
    text = """후킹 문장1: 훅1
후킹 문장2: 훅2
블로그 초안: 첫 문단
둘째 문단
셋째 문단
영상 제목: - 타이틀1
YouTube 제목 - 타이틀2
"""
    parsed = nhu.parse_generated_text(text)
    assert parsed['hook_lines'] == ['훅1', '훅2']
    assert parsed['blog_paragraphs'] == ['첫 문단']
    assert parsed['video_titles'] == ['타이틀1', '타이틀2']
