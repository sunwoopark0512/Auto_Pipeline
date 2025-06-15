import sys
import types
import logging

client_mod = types.ModuleType('notion_client')
class DummyClient:
    def __init__(self, *args, **kwargs):
        pass
client_mod.Client = DummyClient
sys.modules['notion_client'] = client_mod
sys.modules.setdefault('dotenv', types.ModuleType('dotenv'))
sys.modules['dotenv'].load_dotenv = lambda *args, **kwargs: None
logging.FileHandler = lambda *args, **kwargs: logging.NullHandler()

import notion_hook_uploader


def test_parse_generated_text_basic():
    text = (
        "후킹 문장1: Hook1\n"
        "후킹 문장2: Hook2\n"
        "블로그 초안: Para1\nPara2\nPara3\n"
        "영상 제목: Title1\n- Title2\n"
    )
    result = notion_hook_uploader.parse_generated_text(text)
    assert result["hook_lines"] == ["Hook1", "Hook2"]
    assert result["blog_paragraphs"][:1] == ["Para1"]
    assert result["video_titles"][0] == "Title2"


