from unittest.mock import MagicMock, patch
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import auto_rewriter as ar


def test_fetch_low_performers():
    mock_client = MagicMock()
    mock_client.table.return_value.select.return_value.lte.return_value.is_.return_value.execute.return_value.data = [
        {"id": 1, "content": "old", "engagement_score": 0.1, "needs_rewrite": False}
    ]
    with patch("auto_rewriter._get_client", return_value=mock_client):
        rows = ar.fetch_low_performers("content", 0.3)
    assert rows and rows[0]["id"] == 1


def test_rewrite_batch(monkeypatch):
    """GPT 호출·Supabase 업데이트가 모두 불리는지 확인."""
    monkeypatch.setattr(
        "auto_rewriter.fetch_low_performers",
        lambda table, threshold: [{"id": 99, "content": "hello", "topic": "test"}],
    )
    monkeypatch.setattr("auto_rewriter._ask_gpt", lambda txt, topic: "new")
    updated = {}

    def _mock_update(table, row_id, new_content):
        updated["row_id"] = row_id
        updated["content"] = new_content

    monkeypatch.setattr("auto_rewriter.update_rewritten_row", _mock_update)
    ar.rewrite_batch("content", 0.3)
    assert updated["content"] == "new" and updated["row_id"] == 99
