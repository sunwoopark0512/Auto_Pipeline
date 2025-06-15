import os
import requests
from .base_adapter import PublisherAdapter


class MediumAdapter(PublisherAdapter):
    """Medium API 퍼블리셔."""

    def __init__(self):
        self.token = os.getenv("MEDIUM_INTEGRATION_TOKEN")
        self.dryrun = os.getenv("DRYRUN", "false").lower() == "true"

    def publish(self, content: dict) -> str:
        if self.dryrun:
            return "dryrun://medium/post"

        headers = {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}
        response = requests.post(
            "https://api.medium.com/v1/users/me/posts",
            headers=headers,
            json={"title": content["title"], "contentFormat": "html", "content": content["body"], "publishStatus": "public"},
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()
        return data.get("data", {}).get("url", "")
