from __future__ import annotations

from notion_client import Client


class NotionClient:
    """Simple wrapper around the official Notion Client."""

    def __init__(self, token: str, database_id: str) -> None:
        self.client = Client(auth=token)
        self.database_id = database_id

    def create_page(self, properties: dict) -> object:
        """Create a page in the configured database."""
        return self.client.pages.create(
            parent={"database_id": self.database_id},
            properties=properties["properties"] if "properties" in properties else properties,
        )
