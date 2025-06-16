import sys
import types
import os
import importlib
from pathlib import Path

# ensure repository root is on sys.path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

# provide stub modules to satisfy imports in notion_hook_uploader
sys.modules['notion_client'] = types.SimpleNamespace(Client=lambda *a, **k: None)
sys.modules['dotenv'] = types.SimpleNamespace(load_dotenv=lambda: None)

# ensure log directory exists to avoid logging.FileHandler errors
os.makedirs('logs', exist_ok=True)

notion_hook_uploader = importlib.import_module('notion_hook_uploader')
parse_generated_text = notion_hook_uploader.parse_generated_text


def test_parse_typical_output():
    text = (
        "후킹 문장1: 당신의 미래를 바꿀 비밀을 알려드립니다!\n"
        "후킹 문장2: 지금 바로 시작하세요!\n"
        "블로그 초안:\n"
        "첫 번째 문단입니다.\n"
        "두 번째 문단입니다.\n"
        "세 번째 문단입니다.\n"
        "영상 제목: - 첫 번째 영상 제목\n"
        "YouTube 제목: - 두 번째 영상 제목\n"
    )
    parsed = parse_generated_text(text)
    assert parsed['hook_lines'] == [
        '당신의 미래를 바꿀 비밀을 알려드립니다!',
        '지금 바로 시작하세요!'
    ]
    assert parsed['blog_paragraphs'] == [
        '첫 번째 문단입니다.',
        '두 번째 문단입니다.',
        '세 번째 문단입니다.'
    ]
    assert parsed['video_titles'] == ['첫 번째 영상 제목', '두 번째 영상 제목']


def test_parse_malformed_output():
    text = (
        "후킹 문장1: 하나만 있습니다.\n"
        "영상 제목: - 유일한 영상 제목\n"
    )
    parsed = parse_generated_text(text)
    assert parsed['hook_lines'] == ['하나만 있습니다.', '']
    assert parsed['blog_paragraphs'] == ['', '', '']
    assert parsed['video_titles'] == ['유일한 영상 제목', '']
