"""Podcast Creator Tests."""

from datetime import datetime
from pathlib import Path

import pytest

from podcast.creator import PodcastCreator, PodcastEpisode, PodcastSeries


@pytest.fixture
def temp_dir(tmp_path):
    """Temporary directory for tests."""
    return tmp_path


@pytest.fixture
def sample_episode():
    """Sample podcast episode."""
    return PodcastEpisode(
        title="Test Episode",
        description="Test Description",
        audio_file=Path("test.mp3"),
        duration=300,
        published_at=datetime.now().isoformat(),
        tags=["test", "sample"],
    )


@pytest.fixture
def sample_series(sample_episode):
    """Sample podcast series."""
    return PodcastSeries(
        title="Test Series",
        description="Test Series Description",
        author="Test Author",
        episodes=[sample_episode],
    )


def test_create_series(temp_dir, sample_series):
    """Test series creation."""
    creator = PodcastCreator(temp_dir)
    manifest_path = creator.create_series(sample_series)

    assert manifest_path.exists()
    loaded_series = creator.get_series(manifest_path)
    assert loaded_series.title == sample_series.title
    assert loaded_series.description == sample_series.description
    assert len(loaded_series.episodes) == 1


def test_add_episode(temp_dir, sample_series, sample_episode):
    """Test adding episode to series."""
    creator = PodcastCreator(temp_dir)
    manifest_path = creator.create_series(sample_series)

    new_episode = PodcastEpisode(
        title="New Episode",
        description="New Description",
        audio_file=Path("new.mp3"),
        duration=400,
        published_at=datetime.now().isoformat(),
    )

    creator.add_episode(manifest_path, new_episode)
    loaded_series = creator.get_series(manifest_path)
    assert len(loaded_series.episodes) == 2


def test_invalid_series(temp_dir):
    """Test handling of invalid series data."""
    creator = PodcastCreator(temp_dir)
    invalid_series = PodcastSeries(title="", description="", author="Test")

    with pytest.raises(ValueError):
        creator.create_series(invalid_series)


def test_invalid_episode(temp_dir, sample_series):
    """Test handling of invalid episode data."""
    creator = PodcastCreator(temp_dir)
    manifest_path = creator.create_series(sample_series)

    invalid_episode = PodcastEpisode(
        title="",
        description="Test",
        audio_file=Path(""),
        duration=0,
        published_at=datetime.now().isoformat(),
    )

    with pytest.raises(ValueError):
        creator.add_episode(manifest_path, invalid_episode)


def test_nonexistent_series(temp_dir, sample_episode):
    """Test handling of nonexistent series."""
    creator = PodcastCreator(temp_dir)
    with pytest.raises(FileNotFoundError):
        creator.get_series(temp_dir / "nonexistent.json")
