import types
import sys
import logging
import importlib
import os

# Ensure project root is on sys.path
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)


# Mock external libraries to avoid network calls
sys.modules['notion_client'] = types.ModuleType('notion_client')
sys.modules['notion_client'].Client = lambda *args, **kwargs: None
sys.modules['dotenv'] = types.ModuleType('dotenv')
sys.modules['dotenv'].load_dotenv = lambda *args, **kwargs: None

# Replace FileHandler to avoid filesystem writes during import
logging.FileHandler = lambda *args, **kwargs: logging.StreamHandler()

notion_module = importlib.import_module('notion_hook_uploader')
parse_generated_text = notion_module.parse_generated_text


def test_parse_generated_text_basic():
    text = (
        "후킹 문장1: 첫 문장\n"
        "후킹 문장2: 둘째 문장\n"
        "블로그 초안: 문단1\n문단2\n문단3\n"
        "영상 제목: 제목1\n- 제목2"
    )
    result = parse_generated_text(text)
    assert result['hook_lines'] == ['첫 문장', '둘째 문장']
    assert result['blog_paragraphs'] == ['문단1']
    assert result['video_titles'] == ['제목2']

