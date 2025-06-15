import os
from .base_adapter import PublisherAdapter

class YouTubeAdapter(PublisherAdapter):
    def __init__(self):
        self.api_key = os.getenv("YOUTUBE_API_KEY")
        self.channel_id = os.getenv("YOUTUBE_CHANNEL_ID")
        self.dryrun = os.getenv("DRYRUN", "false").lower() == "true"
        self.client = None
        if not self.dryrun:
            import google.auth
            import googleapiclient.discovery
            creds, _ = google.auth.default()
            self.client = googleapiclient.discovery.build(
                "youtube", "v3", credentials=creds, developerKey=self.api_key
            )

    def publish(self, content: dict) -> str:
        if self.dryrun:
            return "https://youtu.be/dryrun"

        video_request = self.client.videos().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "title": content["title"],
                    "description": content.get("description", ""),
                    "tags": content.get("tags", []),
                    "categoryId": "22",
                },
                "status": {"privacyStatus": "public"},
            },
            media_body=content["file_path"],
        )
        response = video_request.execute()
        return f"https://youtu.be/{response['id']}"
