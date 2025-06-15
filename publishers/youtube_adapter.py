"""YouTube adapter utilities and helpers."""
from __future__ import annotations

import requests

from publishers.base_adapter import PublisherAdapter


class YouTubeAdapter(PublisherAdapter):
    """Simple stub for YouTube publishing."""

    def _real_publish(self, content: dict) -> str:
        # Stubbed publish method for testing
        return "https://youtu.be/dummy123"


def get_recent_videos(channel_id: str, api_key: str, limit: int = 5) -> list:
    """Fetch recent videos from a channel via YouTube Data API.

    Parameters
    ----------
    channel_id: str
        The channel ID to query.
    api_key: str
        API key for authenticating with YouTube Data API.
    limit: int, default 5
        Maximum number of results to return.

    Returns
    -------
    list
        List of video items returned by the API.
    """

    url = "https://www.googleapis.com/youtube/v3/search"
    params: dict[str, str | int] = {
        "part": "snippet",
        "channelId": channel_id,
        "maxResults": limit,
        "order": "date",
        "type": "video",
        "key": api_key,
    }
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    return data.get("items", [])
