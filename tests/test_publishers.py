import os
from publishers.youtube_adapter import YouTubeAdapter
from publishers.wordpress_adapter import WordPressAdapter
from publishers.medium_adapter import MediumAdapter


def test_youtube_publish_dryrun(monkeypatch):
    monkeypatch.setenv("DRYRUN", "true")
    monkeypatch.setenv("YOUTUBE_API_KEY", "x")
    monkeypatch.setenv("YOUTUBE_CHANNEL_ID", "x")
    adapter = YouTubeAdapter()
    url = adapter.publish({"title": "t", "description": "d", "file_path": "dummy"})
    assert "dryrun" in url


def test_wordpress_publish_dryrun(monkeypatch):
    monkeypatch.setenv("DRYRUN", "true")
    monkeypatch.setenv("WORDPRESS_BASE_URL", "https://example.com")
    adapter = WordPressAdapter()
    url = adapter.publish({"title": "t", "body": "b"})
    assert "dryrun" in url


def test_medium_publish_dryrun(monkeypatch):
    monkeypatch.setenv("DRYRUN", "true")
    adapter = MediumAdapter()
    url = adapter.publish({"title": "t", "body": "b"})
    assert "dryrun" in url
