"""Utility to update Notion page status."""

from notion_client import Client  # type: ignore  # pylint: disable=import-error

notion = Client(auth="your_notion_token")


def update_notion_status(page_id: str, status: str) -> None:
    """Update the given Notion page's status property."""
    notion.pages.update(
        page_id=page_id,
        properties={
            "Status": {
                "select": {"name": status}
            }
        }
    )
