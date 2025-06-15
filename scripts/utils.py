from datetime import datetime


def truncate_text(text: str, max_length: int = 2000) -> str:
    """Truncate Notion rich_text content to avoid API errors."""
    return text if len(text) <= max_length else text[:max_length]


def create_notion_page(notion, database_id: str, keyword: str, parsed: dict) -> None:
    """Create a Notion page using parsed hook data."""
    topic = keyword.split()[0] if " " in keyword else keyword
    notion.pages.create(
        parent={"database_id": database_id},
        properties={
            "키워드": {"title": [{"text": {"content": keyword}}]},
            "채널": {"select": {"name": topic}},
            "등록일": {"date": {"start": datetime.utcnow().isoformat() + 'Z'}},
            "후킹문1": {"rich_text": [{"text": {"content": truncate_text(parsed.get("hook_lines", ["", ""])[0])}}]},
            "후킹문2": {"rich_text": [{"text": {"content": truncate_text(parsed.get("hook_lines", ["", ""])[1])}}]},
            "블로그초안": {"rich_text": [{"text": {"content": truncate_text('\n'.join(parsed.get("blog_paragraphs", ["", "", ""])))}}]},
            "영상제목": {"rich_text": [{"text": {"content": truncate_text('\n'.join(parsed.get("video_titles", ["", ""])))}}]},
        },
    )
