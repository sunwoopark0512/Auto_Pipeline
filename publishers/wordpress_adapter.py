import os
import json
from .base_adapter import PublisherAdapter

class WordPressAdapter(PublisherAdapter):
    def __init__(self):
        self.token = os.getenv("WORDPRESS_TOKEN")
        self.base_url = os.getenv("WORDPRESS_BASE_URL")

    def _real_publish(self, content: dict) -> str:
        import requests  # type: ignore
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }
        data = {
            "title": content["title"],
            "content": content["html"],
            "status": "publish",
        }
        url = f"{self.base_url}/wp-json/wp/v2/posts"
        res = requests.post(url, headers=headers, data=json.dumps(data))
        res.raise_for_status()
        return res.json().get("link")
