import os
import sys
import types
import importlib

# Ensure repository root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Prepare stubs before module import
dotenv_mod = types.ModuleType('dotenv')
dotenv_mod.load_dotenv = lambda: None
sys.modules['dotenv'] = dotenv_mod

class DummyPages:
    def __init__(self):
        self.created = []
    def create(self, **kwargs):
        self.created.append(kwargs)

class DummyClient:
    def __init__(self, auth=None):
        self.pages = DummyPages()
        self.databases = types.SimpleNamespace(query=lambda **kw: {'results': []})

notion_mod = types.ModuleType('notion_client')
notion_mod.Client = DummyClient
sys.modules['notion_client'] = notion_mod

os.environ['NOTION_API_TOKEN'] = 'token'
os.environ['NOTION_HOOK_DB_ID'] = 'db123'

# Ensure logs directory exists to avoid FileHandler error
os.makedirs('logs', exist_ok=True)

import notion_hook_uploader as nup

def test_create_notion_page(monkeypatch):
    monkeypatch.setattr(nup, 'parse_generated_text', lambda text: {
        'hook_lines': ['a', 'b'],
        'blog_paragraphs': ['p1', 'p2', 'p3'],
        'video_titles': ['v1', 'v2']
    })
    item = {'keyword': 'kw', 'generated_text': 'dummy'}
    nup.create_notion_page(item)
    assert nup.notion.pages.created
    call = nup.notion.pages.created[0]
    assert call['parent']['database_id'] == 'db123'
    assert call['properties']['키워드']['title'][0]['text']['content'] == 'kw'
