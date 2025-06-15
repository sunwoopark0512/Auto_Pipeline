import sys
import types

# Stub external modules at import time so tests can import project modules
if 'dotenv' not in sys.modules:
    dotenv = types.ModuleType('dotenv')
    def load_dotenv(*args, **kwargs):
        return None
    dotenv.load_dotenv = load_dotenv
    sys.modules['dotenv'] = dotenv

if 'openai' not in sys.modules:
    openai = types.ModuleType('openai')
    class ChatCompletion:
        @staticmethod
        def create(*args, **kwargs):
            raise NotImplementedError
    openai.ChatCompletion = ChatCompletion
    openai.api_key = None
    sys.modules['openai'] = openai

if 'notion_client' not in sys.modules:
    notion_client = types.ModuleType('notion_client')
    class DummyPages:
        def create(self, *args, **kwargs):
            return None
    class Client:
        def __init__(self, auth=None):
            self.pages = DummyPages()
            self.databases = types.SimpleNamespace(query=lambda **kw: {'results': []})
    notion_client.Client = Client
    sys.modules['notion_client'] = notion_client

import pytest

@pytest.fixture(autouse=True)
def stub_external_modules(monkeypatch):
    """Ensure stubs remain during tests."""
    yield
