import sys
import types
import importlib
import os

import pytest


def import_hook_module():
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    dummy_dotenv = types.ModuleType('dotenv')
    dummy_dotenv.load_dotenv = lambda *a, **k: None
    sys.modules['dotenv'] = dummy_dotenv
    sys.modules['openai'] = types.ModuleType('openai')
    return importlib.import_module('hook_generator')


def import_notion_module():
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    os.makedirs('logs', exist_ok=True)
    dummy_nc = types.ModuleType('notion_client')
    class DummyClient:
        def __init__(self, *args, **kwargs):
            pass
    dummy_nc.Client = DummyClient
    sys.modules['notion_client'] = dummy_nc
    dummy_dotenv = types.ModuleType('dotenv')
    dummy_dotenv.load_dotenv = lambda *a, **k: None
    sys.modules['dotenv'] = dummy_dotenv
    return importlib.import_module('notion_hook_uploader')


def test_generate_hook_prompt_basic():
    module = import_hook_module()
    prompt = module.generate_hook_prompt(
        keyword='테스트 키워드',
        topic='테스트',
        source='Twitter',
        score=80,
        growth=1.5,
        mentions=100,
    )
    assert '주제: 테스트 키워드' in prompt
    assert '출처: Twitter' in prompt
    assert '트렌드 점수: 80' in prompt


def test_parse_generated_text_extraction():
    module = import_notion_module()
    text = (
        "후킹 문장1: A\n"
        "후킹 문장2: B\n"
        "블로그 초안: 서론\n"
        "첫 문단\n"
        "둘째 문단\n"
        "셋째 문단\n"
        "영상 제목: title1\n"
        "- title2\n"
    )
    result = module.parse_generated_text(text)
    assert result['hook_lines'] == ['A', 'B']
    assert result['blog_paragraphs'][0] == '서론'
    assert result['video_titles'][0] == 'title2'
