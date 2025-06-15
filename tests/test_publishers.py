import pytest
from publishers.youtube_adapter import YouTubeAdapter
from publishers.medium_adapter import MediumAdapter
from publishers.wordpress_adapter import WordPressAdapter

@pytest.fixture(autouse=True)
def set_dryrun(monkeypatch):
    monkeypatch.setenv("DRYRUN", "true")

@pytest.mark.parametrize("adapter_cls", [
    YouTubeAdapter,
    MediumAdapter,
    WordPressAdapter,
])
def test_publish_dryrun(adapter_cls):
    adapter = adapter_cls()
    url = adapter.publish({
        "title": "test",
        "description": "",
        "html": "",
        "file_path": "dummy.mp4",
    })
    assert url == "DRYRUN_URL"
