"""Podcast Creator Module."""

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List


@dataclass
class PodcastEpisode:
    """Podcast episode data structure."""

    title: str
    description: str
    audio_file: Path
    duration: int  # in seconds
    published_at: str
    tags: List[str] = None

    def to_dict(self) -> Dict:
        """Convert episode to dictionary.

        Returns:
            Dict: Episode data as dictionary
        """
        return {
            "title": self.title,
            "description": self.description,
            "audio_file": str(self.audio_file),
            "duration": self.duration,
            "published_at": self.published_at,
            "tags": self.tags or [],
        }


@dataclass
class PodcastSeries:
    """Podcast series data structure."""

    title: str
    description: str
    author: str
    language: str = "en"
    episodes: List[PodcastEpisode] = None

    def to_dict(self) -> Dict:
        """Convert series to dictionary.

        Returns:
            Dict: Series data as dictionary
        """
        return {
            "title": self.title,
            "description": self.description,
            "author": self.author,
            "language": self.language,
            "episodes": [ep.to_dict() for ep in (self.episodes or [])],
        }


class PodcastCreator:
    """Podcast creation and management tool."""

    def __init__(self, output_dir: Path) -> None:
        """Initialize podcast creator.

        Args:
            output_dir: Directory for podcast output files
        """
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def create_series(self, series: PodcastSeries) -> Path:
        """Create a new podcast series.

        Args:
            series: Podcast series data

        Returns:
            Path: Path to the created series manifest

        Raises:
            ValueError: If series data is invalid
        """
        if not series.title or not series.description:
            raise ValueError("Series title and description are required")

        manifest_path = (
            self.output_dir / f"{series.title.lower().replace(' ', '_')}.json"
        )
        manifest_path.write_text(json.dumps(series.to_dict(), indent=2))
        return manifest_path

    def add_episode(self, series_path: Path, episode: PodcastEpisode) -> None:
        """Add an episode to existing series.

        Args:
            series_path: Path to series manifest
            episode: Episode to add

        Raises:
            FileNotFoundError: If series manifest doesn't exist
            ValueError: If episode data is invalid
        """
        if not series_path.exists():
            raise FileNotFoundError(f"Series manifest not found: {series_path}")

        if not episode.title or not episode.audio_file:
            raise ValueError("Episode title and audio file are required")

        data = json.loads(series_path.read_text())
        episodes = data.get("episodes", [])
        episodes.append(episode.to_dict())
        data["episodes"] = episodes
        series_path.write_text(json.dumps(data, indent=2))

    def get_series(self, series_path: Path) -> PodcastSeries:
        """Load podcast series from manifest.

        Args:
            series_path: Path to series manifest

        Returns:
            PodcastSeries: Loaded series data

        Raises:
            FileNotFoundError: If series manifest doesn't exist
        """
        if not series_path.exists():
            raise FileNotFoundError(f"Series manifest not found: {series_path}")

        data = json.loads(series_path.read_text())
        episodes = []
        for ep_data in data.get("episodes", []):
            episodes.append(
                PodcastEpisode(
                    title=ep_data["title"],
                    description=ep_data["description"],
                    audio_file=Path(ep_data["audio_file"]),
                    duration=ep_data["duration"],
                    published_at=ep_data["published_at"],
                    tags=ep_data.get("tags", []),
                )
            )

        return PodcastSeries(
            title=data["title"],
            description=data["description"],
            author=data["author"],
            language=data.get("language", "en"),
            episodes=episodes,
        )
