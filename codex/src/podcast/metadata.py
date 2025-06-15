"""Podcast metadata models."""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class EpisodeMetadata:
    """Metadata for a podcast episode."""

    title: str
    description: str
    published_at: datetime
