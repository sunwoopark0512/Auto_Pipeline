import os
from .base_adapter import PublisherAdapter

class YouTubeAdapter(PublisherAdapter):
    """YouTube 업로드 어댑터"""

    def __init__(self):
        self.client = None  # Lazy initialization

    def _build_client(self):
        if not self.client:
            from googleapiclient.discovery import build  # type: ignore
            api_key = os.getenv("YOUTUBE_API_KEY")
            self.client = build("youtube", "v3", developerKey=api_key)

    def _real_publish(self, content: dict) -> str:
        self._build_client()
        video_req = self.client.videos().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "title": content.get("title", ""),
                    "description": content.get("description", ""),
                },
                "status": {"privacyStatus": "public"},
            },
            media_body=content["file_path"],
        )
        res = video_req.execute()
        return f"https://youtu.be/{res['id']}"
