import sys
import logging
import types

sys.modules["dotenv"] = types.SimpleNamespace(load_dotenv=lambda: None)
logging.FileHandler = lambda *a, **k: logging.StreamHandler()

class DummyClient:
    def __init__(self, *args, **kwargs):
        pass

sys.modules['notion_client'] = types.SimpleNamespace(Client=DummyClient)

import notion_hook_uploader


def test_parse_generated_text_basic():
    text = (
        "후킹 문장1: 첫번째 후킹\n"
        "후킹 문장2: 두번째 후킹\n"
        "블로그 초안: 첫문단\n둘째문단\n셋째문단\n"
        "영상 제목: - 제목A\n- 제목B"
    )
    parsed = notion_hook_uploader.parse_generated_text(text)
    assert parsed['hook_lines'][0] == '첫번째 후킹'
    assert parsed['hook_lines'][1] == '두번째 후킹'
    assert parsed['blog_paragraphs'][0] == '첫문단'
    assert parsed['video_titles'][0]
