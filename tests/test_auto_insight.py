from unittest.mock import MagicMock, patch

import auto_insight as ai


def test_summarize_metrics():
    import pandas as pd

    df = pd.DataFrame(
        [
            {"id": 1, "engagement_score": 0.1},
            {"id": 2, "engagement_score": 0.9},
        ]
    )
    stats = ai.summarize_metrics(df)
    assert stats["avg"] == 0.5 and stats["count"] == 2


def test_generate_insight(monkeypatch):
    # mock data fetch
    monkeypatch.setattr(
        "auto_insight.fetch_range",
        lambda table, days: __import__("pandas").DataFrame(
            [{"id": 1, "engagement_score": 0.4}]
        ),
    )
    # mock GPT
    monkeypatch.setattr("auto_insight.gpt_insight", lambda stats, horizon: "INSIGHT")
    created = {}

    def _mock_publish(db_id, title, text, stats):
        created["title"] = title
        created["text"] = text

    monkeypatch.setattr("auto_insight.notion_publish", _mock_publish)
    ai.generate_insight("content", 7, "fake_db")
    assert created["text"] == "INSIGHT"
