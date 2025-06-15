import os
import requests
from .base_adapter import PublisherAdapter

class MediumAdapter(PublisherAdapter):
    def __init__(self):
        self.token = os.getenv("MEDIUM_INTEGRATION_TOKEN")
        self.dryrun = os.getenv("DRYRUN", "false").lower() == "true"

    def publish(self, content: dict) -> str:
        if self.dryrun:
            return "https://medium.com/dryrun"

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }
        response = requests.post(
            "https://api.medium.com/v1/users/me/posts",
            headers=headers,
            json={
                "title": content["title"],
                "contentFormat": "html",
                "content": content.get("body", ""),
                "publishStatus": "public",
            },
            timeout=30,
        )
        response.raise_for_status()
        return response.json()["data"]["url"]
