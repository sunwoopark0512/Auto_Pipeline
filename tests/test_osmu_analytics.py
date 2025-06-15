import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from unittest.mock import MagicMock
import osmu_analytics as oa
import pandas as pd

FAKE_DATA = [
    {"id":1, "youtube_views":100, "medium_reads":50, "x_engagement":20, "tistory_views":80, "published_at": "2025-06-10T00:00:00Z"},
    {"id":2, "youtube_views":10,  "medium_reads":5,  "x_engagement":2,  "tistory_views":8,  "published_at": "2025-06-11T00:00:00Z"},
]

def test_compute_priority():
    df = pd.DataFrame(FAKE_DATA)
    out = oa.compute_priority(df.copy())
    assert "priority_score" in out
    assert out.loc[out["id"]==1, "priority_score"].iloc[0] > out.loc[out["id"]==2, "priority_score"].iloc[0]

def test_process(monkeypatch):
    monkeypatch.setenv("SUPABASE_URL", "url")
    monkeypatch.setenv("SUPABASE_ANON_KEY", "key")
    mock_client = MagicMock()
    mock_table = MagicMock()
    mock_client.table.return_value = mock_table
    monkeypatch.setattr("osmu_analytics._get_client", lambda: mock_client)
    df = pd.DataFrame(FAKE_DATA)
    monkeypatch.setattr("osmu_analytics.fetch_recent", lambda t,d,l: df)
    updated = []
    def fake_execute():
        return MagicMock()
    def fake_upsert(props, on_conflict=None):
        updated.append(props)
        m = MagicMock()
        m.execute = fake_execute
        return m
    mock_table.upsert.side_effect = fake_upsert
    oa.process("content", 7, 10)
    assert any(item["content_id"]==1 for item in updated)
