import importlib
from unittest.mock import MagicMock


def test_fetch_pending(monkeypatch):
    monkeypatch.setenv("SUPABASE_URL", "url")
    monkeypatch.setenv("SUPABASE_ANON_KEY", "key")
    monkeypatch.setenv("PODCAST_RSS_FILE", "tmp.xml")
    import podcast_creator as pc
    importlib.reload(pc)
    mock_supa = MagicMock()
    mock_supa.table.return_value.select.return_value.eq.return_value.is_.return_value.limit.return_value.execute.return_value.data = [
        {"id": 1, "content": "Hello", "title": "Test", "generate_podcast": True, "podcast_generated": False}
    ]
    monkeypatch.setattr("podcast_creator._get_client", lambda: mock_supa)
    rows = pc.fetch_pending("content", 1)
    assert rows and rows[0]["id"] == 1


def test_process_batch(monkeypatch, tmp_path):
    monkeypatch.setenv("SUPABASE_URL", "url")
    monkeypatch.setenv("SUPABASE_ANON_KEY", "key")
    rss_file = tmp_path/"rss.xml"
    monkeypatch.setenv("PODCAST_RSS_FILE", str(rss_file))
    import podcast_creator as pc
    importlib.reload(pc)
    # mock fetch
    monkeypatch.setattr("podcast_creator.fetch_pending", lambda t, l: [{"id": 2, "content": "Hi", "title": "T"}])
    # mock TTS & upload
    audio_path = tmp_path/"f.mp3"
    audio_path.write_bytes(b"test")
    monkeypatch.setattr("podcast_creator.generate_audio", lambda text: str(audio_path))
    mock_supa = MagicMock()
    mock_supa.storage.from_.return_value.get_public_url.return_value = {"publicURL": "http://audio.mp3"}
    mock_supa.storage.from_.return_value.upload.return_value = None
    monkeypatch.setattr("podcast_creator._get_client", lambda: mock_supa)
    # mock append_rss to file
    pc.process_batch("content", 1)
    assert rss_file.exists()
