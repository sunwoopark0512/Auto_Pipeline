from datetime import datetime


def truncate_text(text: str, max_length: int = 2000) -> str:
    """Truncate text for Notion rich text fields."""
    return text if len(text) <= max_length else text[:max_length]


def create_hook_page(notion_client, database_id: str, item: dict) -> None:
    """Create a Notion page for a generated marketing hook.

    Parameters
    ----------
    notion_client : notion_client.Client-like
        Client used to call the Notion API.
    database_id : str
        ID of the Notion database where the page will be created.
    item : dict
        Dictionary containing at minimum a ``keyword`` field and parsed
        hook data. Parsed data can be provided via the ``parsed`` key or
        the legacy ``hook_lines``/``blog_paragraphs``/``video_titles``
        keys.
    """
    keyword = item.get("keyword")
    if not keyword:
        raise ValueError("keyword is required")

    topic = keyword.split()[0] if " " in keyword else keyword

    parsed = item.get("parsed") or {
        "hook_lines": item.get("hook_lines", ["", ""]),
        "blog_paragraphs": item.get("blog_paragraphs", ["", "", ""]),
        "video_titles": item.get("video_titles", ["", ""]),
    }

    notion_client.pages.create(
        parent={"database_id": database_id},
        properties={
            "키워드": {"title": [{"text": {"content": keyword}}]},
            "채널": {"select": {"name": topic}},
            "등록일": {"date": {"start": datetime.utcnow().isoformat() + 'Z'}},
            "후킹문1": {
                "rich_text": [
                    {"text": {"content": truncate_text(parsed["hook_lines"][0])}}
                ]
            },
            "후킹문2": {
                "rich_text": [
                    {"text": {"content": truncate_text(parsed["hook_lines"][1])}}
                ]
            },
            "블로그초안": {
                "rich_text": [
                    {
                        "text": {
                            "content": truncate_text(
                                "\n".join(parsed["blog_paragraphs"])
                            )
                        }
                    }
                ]
            },
            "영상제목": {
                "rich_text": [
                    {
                        "text": {
                            "content": truncate_text(
                                "\n".join(parsed["video_titles"])
                            )
                        }
                    }
                ]
            },
        },
    )

