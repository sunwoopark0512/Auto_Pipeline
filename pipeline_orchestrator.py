from publishers.youtube_adapter import YouTubeAdapter
from publishers.wordpress_adapter import WordPressAdapter
from publishers.medium_adapter import MediumAdapter

ADAPTERS = {
    "YouTube": YouTubeAdapter(),
    "WordPress": WordPressAdapter(),
    "Medium": MediumAdapter(),
}

def publish_content(generated: dict, channel: str) -> str:
    adapter = ADAPTERS[channel]
    return adapter.publish(generated)
