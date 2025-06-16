import os
import sys
import types
import importlib
import pytest

# Fixture to load hook_generator with stubbed dependencies
@pytest.fixture
def hook_generator_module(monkeypatch):
    monkeypatch.syspath_prepend(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    monkeypatch.setitem(sys.modules, 'openai', types.ModuleType('openai'))
    dotenv = types.ModuleType('dotenv')
    dotenv.load_dotenv = lambda *a, **k: None
    monkeypatch.setitem(sys.modules, 'dotenv', dotenv)
    if 'hook_generator' in sys.modules:
        del sys.modules['hook_generator']
    return importlib.import_module('hook_generator')

# Fixture to load notion_hook_uploader with stubbed dependencies
@pytest.fixture
def notion_hook_module(monkeypatch, tmp_path):
    monkeypatch.syspath_prepend(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    monkeypatch.setitem(sys.modules, 'openai', types.ModuleType('openai'))
    dotenv = types.ModuleType('dotenv')
    dotenv.load_dotenv = lambda *a, **k: None
    monkeypatch.setitem(sys.modules, 'dotenv', dotenv)
    mod_nc = types.ModuleType('notion_client')
    class DummyClient:
        def __init__(self, *a, **k):
            pass
    mod_nc.Client = DummyClient
    monkeypatch.setitem(sys.modules, 'notion_client', mod_nc)
    os.makedirs('logs', exist_ok=True)
    if 'notion_hook_uploader' in sys.modules:
        del sys.modules['notion_hook_uploader']
    return importlib.import_module('notion_hook_uploader')

def test_generate_hook_prompt_inserts_values(hook_generator_module):
    prompt = hook_generator_module.generate_hook_prompt('키워드', 'topic', '트위터', 10, 5, 100)
    assert '주제: 키워드' in prompt
    assert '출처: 트위터' in prompt
    assert '트렌드 점수: 10' in prompt
    assert '성장률: 5' in prompt
    assert '트윗 수: 100' in prompt


def test_parse_generated_text_parses_sections(notion_hook_module):
    text = (
        '후킹문장1: Hook1\n'
        '후킹 문장2 - Hook2\n'
        '블로그 초안:\n'
        'Paragraph1\n'
        'Paragraph2\n'
        'Paragraph3\n'
        '영상 제목: Title1\n'
        '- Title2\n'
        'YouTube 제목 - Title3'
    )
    parsed = notion_hook_module.parse_generated_text(text)
    assert parsed['hook_lines'] == ['Hook1', 'Hook2']
    assert parsed['blog_paragraphs'][0] == 'Paragraph1'
    assert parsed['video_titles'] == ['Title2', 'Title3']


def test_parse_generated_text_empty(notion_hook_module):
    parsed = notion_hook_module.parse_generated_text('')
    assert parsed == {
        'hook_lines': ['', ''],
        'blog_paragraphs': ['', '', ''],
        'video_titles': ['', '']
    }
