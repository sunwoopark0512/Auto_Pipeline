import os
import sys
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
import graphic_generator as gg

FAKE_ROW = {"id": 7, "content": "Deep dive into AI.", "title": "AI 101", "generate_graphic": True, "graphic_generated": False}


def test_fetch_pending(monkeypatch):
    mock_supa = MagicMock()
    mock_supa.table.return_value.select.return_value.eq.return_value.is_.return_value.limit.return_value.execute.return_value.data = [FAKE_ROW]
    monkeypatch.setenv("SUPABASE_URL","url"); monkeypatch.setenv("SUPABASE_ANON_KEY","key")
    monkeypatch.setattr("graphic_generator._get_client", lambda: mock_supa)
    rows = gg.fetch_pending("content", 1)
    assert rows[0]["id"] == 7


def test_process_batch(monkeypatch, tmp_path):
    monkeypatch.setattr("graphic_generator.fetch_pending", lambda t,l: [FAKE_ROW])
    monkeypatch.setenv("OPENAI_API_KEY","key")
    fake_url = "https://img.example.com/1.png"
    monkeypatch.setattr("graphic_generator.generate_image", lambda p: fake_url)
    dummy_bytes = tmp_path/"f.png"
    dummy_bytes.write_bytes(b"123")
    monkeypatch.setattr("graphic_generator.download_image", lambda u: open(dummy_bytes, "rb"))
    mock_supa = MagicMock()
    mock_supa.storage.from_.return_value.get_public_url.return_value = {"publicURL": "https://cdn/1.png"}
    mock_supa.storage.from_.return_value.upload.return_value = None
    monkeypatch.setattr("graphic_generator._get_client", lambda: mock_supa)
    updated = {}
    monkeypatch.setattr("graphic_generator.update_row", lambda t,i,url: updated.update({"id": i, "url": url}))
    gg.process_batch("content",1)
    assert updated["id"] == 7 and updated["url"].startswith("https://cdn/")
