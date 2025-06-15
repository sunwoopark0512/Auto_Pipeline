"""Lightweight Notion API wrapper used for logging to Notion databases."""

import requests


class NotionClient:
    """Simple wrapper for the Notion API"""

    def __init__(self, notion_token: str, database_id: str):
        self.api_url = "https://api.notion.com/v1/pages"
        self.database_id = database_id
        self.headers = {
            "Authorization": f"Bearer {notion_token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        }

    def create_page(self, payload: dict) -> requests.Response:
        """Send a request to create a new page."""
        return requests.post(
            self.api_url, headers=self.headers, json=payload, timeout=10
        )
