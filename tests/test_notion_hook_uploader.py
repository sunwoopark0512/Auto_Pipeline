import sys
import logging
from types import SimpleNamespace
import importlib

sys.modules['dotenv'] = SimpleNamespace(load_dotenv=lambda: None)
sys.modules['notion_client'] = SimpleNamespace(Client=lambda **k: 'client')
logging.FileHandler = lambda *a, **kw: logging.NullHandler()
if 'notion_hook_uploader' in sys.modules:
    del sys.modules['notion_hook_uploader']
import notion_hook_uploader


def test_parse_generated_text():
    text = """후킹 문장1: Hook1\n후킹 문장2: Hook2\n블로그 초안: Para1\nPara2\nPara3\n영상 제목:\n- Video1\n- Video2"""
    parsed = notion_hook_uploader.parse_generated_text(text)
    assert parsed['hook_lines'] == ['Hook1', 'Hook2']
    assert parsed['blog_paragraphs'][0] == 'Para1'
    assert parsed['video_titles'][0] == 'Video2'
