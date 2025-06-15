"""Utilities for syncing status to Notion."""

from notion_client import Client


def update_notion_status(notion_token: str, page_id: str, status: str):
    """Update the status property of a Notion page."""
    notion = Client(auth=notion_token)
    notion.pages.update(
        page_id=page_id,
        properties={"Status": {"select": {"name": status}}}
    )
