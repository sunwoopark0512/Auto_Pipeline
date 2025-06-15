import os
from notion_client import Client


NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DB_ID = os.getenv("NOTION_DB_ID")

def create_content_page(data: dict):
    client = Client(auth=NOTION_TOKEN)
    properties = {
        "Content ID": {"title": [{"text": {"content": data.get("id")}}]},
        "Keyword/Topic": {"rich_text": [{"text": {"content": data.get("keyword")}}]},
        "Platform": {"select": {"name": data.get("platform")}},
        "Status": {"select": {"name": data.get("status")}},
        "Slice Index": {"number": data.get("slice_index")},
        "URL": {"url": data.get("url")},
        "Created At": {"date": {"start": data.get("created_at")}},
    }
    if data.get("engagement") is not None:
        properties["Engagement Score"] = {"number": data["engagement"]}
    client.pages.create(parent={"database_id": NOTION_DB_ID}, properties=properties)
