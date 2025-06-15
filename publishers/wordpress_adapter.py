import os
import requests
from .base_adapter import PublisherAdapter

class WordPressAdapter(PublisherAdapter):
    def __init__(self):
        self.base_url = os.getenv("WORDPRESS_BASE_URL")
        self.user = os.getenv("WORDPRESS_API_USER")
        self.password = os.getenv("WORDPRESS_API_PASSWORD")
        self.dryrun = os.getenv("DRYRUN", "false").lower() == "true"

    def publish(self, content: dict) -> str:
        if self.dryrun:
            return f"{self.base_url}/dryrun"

        response = requests.post(
            f"{self.base_url}/wp-json/wp/v2/posts",
            auth=(self.user, self.password),
            json={
                "title": content["title"],
                "content": content.get("body", ""),
                "status": "publish",
            },
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()
        return data.get("link", "")
