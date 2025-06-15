import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from unittest.mock import patch, MagicMock
import ab_variant_manager as avm

FAKE_ROW = {"id": 10, "title": "Hello World", "content": "This is a test content."}


def test_fetch_rows(monkeypatch):
    mock_supa = MagicMock()
    mock_supa.table.return_value.select.return_value.is_.return_value.limit.return_value.execute.return_value.data = [FAKE_ROW]
    monkeypatch.setenv("SUPABASE_URL", "url")
    monkeypatch.setenv("SUPABASE_ANON_KEY", "key")
    monkeypatch.setattr("ab_variant_manager._get_client", lambda: mock_supa)
    rows = avm.fetch_rows("content", 1)
    assert rows[0]["id"] == 10


def test_generate_variants_for_row(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "key")
    monkeypatch.setattr("ab_variant_manager._ask_variants", lambda prompt: ["V1", "V2", "V3"])
    out = avm.generate_variants_for_row(FAKE_ROW, 3, 2)
    assert len(out["title_variants"]) == 3
    assert len(out["thumb_text_variants"]) == 2


def test_process_batch(monkeypatch):
    monkeypatch.setenv("SUPABASE_URL", "url")
    monkeypatch.setenv("SUPABASE_ANON_KEY", "key")
    monkeypatch.setattr("ab_variant_manager.fetch_rows", lambda t, l: [FAKE_ROW])
    monkeypatch.setattr(
        "ab_variant_manager.generate_variants_for_row",
        lambda row, tn, th: {"title_variants": ["A"], "thumb_text_variants": ["B"]},
    )
    updated = {}
    monkeypatch.setattr("ab_variant_manager.update_row", lambda t, i, u: updated.update(u))
    avm.process_batch("content", 1, 1, 1)
    assert "title_variants" in updated and "thumb_text_variants" in updated
