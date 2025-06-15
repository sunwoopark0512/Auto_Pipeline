import os
import json
from .base_adapter import PublisherAdapter

class MediumAdapter(PublisherAdapter):
    def __init__(self):
        self.token = os.getenv("MEDIUM_INTEGRATION_TOKEN")

    def _real_publish(self, content: dict) -> str:
        import requests  # type: ignore
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }
        data = {
            "title": content["title"],
            "contentFormat": "html",
            "content": content["html"],
            "publishStatus": "public",
        }
        res = requests.post(
            "https://api.medium.com/v1/users/me/posts",
            headers=headers,
            data=json.dumps(data),
        )
        res.raise_for_status()
        return res.json()["data"]["url"]
