"""Notion 페이지 삭제 스크립트."""
import os
import logging
from typing import Any, Optional
from notion_client import Client
from dotenv import load_dotenv

load_dotenv()

NOTION_TOKEN: Optional[str] = os.getenv("NOTION_API_TOKEN")
NOTION_HOOK_DB_ID: Optional[str] = os.getenv("NOTION_HOOK_DB_ID")

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')
if not NOTION_TOKEN or not NOTION_HOOK_DB_ID:
    logging.warning("⚠️ NOTION 관련 환경 변수가 누락되었습니다. 일부 기능이 제한될 수 있습니다.")
notion = Client(auth=NOTION_TOKEN)

def find_page_id_by_keyword(keyword: str) -> Optional[str]:
    """주어진 키워드를 가진 페이지 ID를 반환합니다."""
    try:
        query: Any = notion.databases.query(
            database_id=NOTION_HOOK_DB_ID,
            filter={"property": "키워드", "title": {"equals": keyword}},
            page_size=1,
        )
        results = query.get("results", [])
        if results:
            return results[0]["id"]
        return None
    except Exception as exc:  # pragma: no cover - 실제 API 에러는 테스트에서 모킹됨
        logging.error("❌ 페이지 검색 실패: %s", exc)
        return None

def delete_page(page_id: str) -> bool:
    """페이지를 아카이브 처리하여 사실상 삭제합니다."""
    try:
        notion.pages.update(page_id, archived=True)
        logging.info("🗑️ 삭제 완료: %s", page_id)
        return True
    except Exception as exc:  # pragma: no cover - 실제 API 에러는 테스트에서 모킹됨
        logging.error("❌ 삭제 실패: %s", exc)
        return False

def delete_by_keyword(keyword: str) -> bool:
    """키워드로 페이지를 찾아 삭제한다."""
    page_id = find_page_id_by_keyword(keyword)
    if not page_id:
        logging.warning("⚠️ 해당 키워드의 페이지를 찾을 수 없습니다: %s", keyword)
        return False
    return delete_page(page_id)

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("사용법: python delete_notion_page.py <키워드>")
        sys.exit(1)

    delete_by_keyword(sys.argv[1])
