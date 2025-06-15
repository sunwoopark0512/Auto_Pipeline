"""Tests for YouTube adapter."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from unittest.mock import Mock

import requests

from publishers.youtube_adapter import get_recent_videos, YouTubeAdapter


def test_get_recent_videos(monkeypatch):
    """Ensure recent videos are fetched correctly."""
    dummy_items = [{"id": {"videoId": "abc"}}, {"id": {"videoId": "def"}}]

    mock_response = Mock()
    mock_response.json.return_value = {"items": dummy_items}
    mock_response.raise_for_status = Mock()

    def fake_get(url, params=None, timeout=10):
        assert params["channelId"] == "chan123"
        assert params["key"] == "apikey"
        return mock_response

    monkeypatch.setattr(requests, "get", fake_get)

    result = get_recent_videos("chan123", "apikey", limit=2)
    assert result == dummy_items


def test_publish_dryrun(monkeypatch, capsys):
    """Validate DRYRUN publishes no content."""
    monkeypatch.setenv("DRYRUN", "true")
    import publishers.base_adapter as base_adapter
    monkeypatch.setattr(base_adapter, "DRYRUN", True)
    adapter = YouTubeAdapter()
    result = adapter.publish({"dummy": "data"})
    assert result == "DRYRUN_URL"
    captured = capsys.readouterr()
    assert "skip upload" in captured.out
