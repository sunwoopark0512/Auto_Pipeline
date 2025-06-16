import logging
from notion_client import Client


def truncate_text(text: str, max_length: int = 2000) -> str:
    """Truncate text for Notion rich_text fields."""
    return text if len(text) <= max_length else text[:max_length]


def page_exists(notion: Client, database_id: str, keyword: str) -> bool:
    """Check if a page with the given keyword already exists in the database."""
    try:
        query = notion.databases.query(
            database_id=database_id,
            filter={"property": "키워드", "title": {"equals": keyword}},
            page_size=1,
        )
        return len(query.get("results", [])) > 0
    except Exception as e:
        logging.warning(f"⚠️ 중복 확인 실패: {keyword} - {e}")
        return False


