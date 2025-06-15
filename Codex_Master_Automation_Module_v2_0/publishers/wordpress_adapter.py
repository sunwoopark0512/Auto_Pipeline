import os
import requests
from .base_adapter import PublisherAdapter


class WordPressAdapter(PublisherAdapter):
    """WordPress REST API 퍼블리셔."""

    def __init__(self):
        self.base_url = os.getenv("WORDPRESS_BASE_URL")
        self.user = os.getenv("WORDPRESS_API_USER")
        self.password = os.getenv("WORDPRESS_API_PASSWORD")
        self.dryrun = os.getenv("DRYRUN", "false").lower() == "true"

    def publish(self, content: dict) -> str:
        if self.dryrun:
            return "dryrun://wordpress/post"

        url = f"{self.base_url}/wp-json/wp/v2/posts"
        response = requests.post(
            url,
            auth=(self.user, self.password),
            json={"title": content["title"], "content": content["body"], "status": "publish"},
            timeout=10,
        )
        response.raise_for_status()
        return response.json().get("link", "")
