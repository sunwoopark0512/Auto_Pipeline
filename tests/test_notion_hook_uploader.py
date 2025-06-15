import json
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
import os
os.makedirs('logs', exist_ok=True)
import importlib
nhu = importlib.import_module('notion_hook_uploader')


def test_parse_generated_text_basic():
    text = """후킹문장1: first\n후킹문장2: second\n블로그 초안: para1\npara2\npara3\n영상 제목: vid1\n- vid2"""
    result = nhu.parse_generated_text(text)
    assert result['hook_lines'][0] == 'first'
    assert result['blog_paragraphs'][0] == 'para1'
    assert result['video_titles']


def test_page_exists_true(monkeypatch):
    class DummyDB:
        def query(self, **kwargs):
            return {'results': [1]}
    monkeypatch.setattr(nhu, 'notion', type('N', (), {'databases': DummyDB()}))
    assert nhu.page_exists('kw') is True


def test_page_exists_exception(monkeypatch):
    class DummyDB:
        def query(self, **kwargs):
            raise RuntimeError('err')
    monkeypatch.setattr(nhu, 'notion', type('N', (), {'databases': DummyDB()}))
    assert nhu.page_exists('kw') is False


def test_upload_all_hooks_retry(monkeypatch, tmp_path):
    data = [{'keyword': 'k', 'generated_text': '후킹문장1: a\n후킹문장2: b'}]
    f = tmp_path / 'hooks.json'
    f.write_text(json.dumps(data))
    monkeypatch.setattr(nhu, 'NOTION_TOKEN', 'x')
    monkeypatch.setattr(nhu, 'NOTION_HOOK_DB_ID', 'db')
    monkeypatch.setattr(nhu, 'HOOK_JSON_PATH', str(f))
    calls = {'n': 0}

    def fake_create(item):
        calls['n'] += 1
        if calls['n'] < 2:
            raise RuntimeError('fail')
    monkeypatch.setattr(nhu, 'create_notion_page', fake_create)
    monkeypatch.setattr(nhu, 'page_exists', lambda x: False)
    nhu.upload_all_hooks()
    assert calls['n'] == 2
