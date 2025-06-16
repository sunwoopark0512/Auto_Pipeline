import sys
import types
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Ensure logs directory exists for FileHandler
os.makedirs('logs', exist_ok=True)

# Mock external modules
notion_client = types.ModuleType('notion_client')
class DummyClient:
    def __init__(self, *args, **kwargs):
        pass
notion_client.Client = DummyClient
sys.modules['notion_client'] = notion_client

sys.modules['dotenv'] = types.ModuleType('dotenv')
sys.modules['dotenv'].load_dotenv = lambda: None

from notion_hook_uploader import parse_generated_text


def test_parse_generated_text_basic():
    sample = (
        "후킹 문장1: 첫번째 후킹\n"
        "후킹문장2: 두번째 후킹\n"
        "블로그 초안:\n"
        "첫 문단\n"
        "둘째 문단\n"
        "셋째 문단\n"
        "영상 제목:\n"
        "- 제목A\n"
        "- 제목B\n"
    )

    result = parse_generated_text(sample)
    assert result["hook_lines"] == ["첫번째 후킹", "두번째 후킹"]
    assert result["blog_paragraphs"] == ["첫 문단"]
    assert result["video_titles"] == ["제목B"]

