"""Podcast feed utilities."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class Episode:
    """Represents a podcast episode."""

    title: str
    audio_path: str
    publish_date: datetime


@dataclass
class Feed:
    """Simple podcast feed container."""

    title: str
    description: str
    episodes: List[Episode] = field(default_factory=list)

    def add_episode(self, episode: Episode) -> None:
        """Add an episode to the feed."""
        self.episodes.append(episode)

    def get_latest_episode(self) -> Optional[Episode]:
        """Return the most recently published episode."""
        if not self.episodes:
            return None
        return max(self.episodes, key=lambda e: e.publish_date)
