from datetime import datetime

from podcast.metadata import EpisodeMetadata


def test_episode_metadata_fields():
    meta = EpisodeMetadata("Ep1", "Desc", datetime(2023, 1, 1))
    assert meta.title == "Ep1"
    assert meta.description == "Desc"
    assert isinstance(meta.published_at, datetime)
