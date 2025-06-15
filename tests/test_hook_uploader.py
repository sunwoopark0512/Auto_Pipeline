import sys
import os; sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import types
from unittest.mock import MagicMock

# fake supabase module
fake_supabase = types.ModuleType("supabase")
fake_supabase.create_client = MagicMock()
sys.modules["supabase"] = fake_supabase

# stub uploader classes to avoid external deps
fake_plugins = types.ModuleType("uploader_plugins")
class DummyUploader:
    def __init__(self):
        pass
    def upload(self, row):
        return "id", "url"

fake_plugins.YouTubeUploader = DummyUploader
fake_plugins.MediumUploader = DummyUploader
fake_plugins.XUploader = DummyUploader
fake_plugins.TistoryUploader = DummyUploader
fake_plugins.BaseUploader = DummyUploader
sys.modules["uploader_plugins"] = fake_plugins

import hook_uploader as hu


def test_pick_channel_custom_pref():
    row = {"preferred_channels": ["medium", "x"]}
    assert hu.pick_channel(row) == "medium"


def test_publish_batch(monkeypatch):
    row = {
        "id": 1,
        "title": "Hi",
        "content": "hello",
        "preferred_channels": ["x"],
        "publish_ready": True,
        "published": False,
    }

    monkeypatch.setattr("hook_uploader.fetch_ready_rows", lambda t, l: [row])
    monkeypatch.setattr(
        "hook_uploader.XUploader.upload", lambda self, r: ("123", "http://x.com/123")
    )
    updated = {}

    def _mock_update(table, row_id, channel, remote_id, public_url):
        updated["channel"] = channel
        updated["url"] = public_url

    monkeypatch.setattr("hook_uploader.update_row", _mock_update)
    hu.publish_batch("content", 1)
    assert updated["channel"] == "x"
