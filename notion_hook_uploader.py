import os
import json
import time
import logging
import re
from datetime import datetime
from notion_client import Client
from retry_helper import call_with_backoff
from dotenv import load_dotenv

# ---------------------- 설정 로딩 ----------------------
load_dotenv()
NOTION_TOKEN = os.getenv("NOTION_API_TOKEN")
NOTION_HOOK_DB_ID = os.getenv("NOTION_HOOK_DB_ID")
HOOK_JSON_PATH = os.getenv("HOOK_OUTPUT_PATH", "data/generated_hooks.json")
FAILED_OUTPUT_PATH = "data/upload_failed_hooks.json"
UPLOAD_DELAY = float(os.getenv("UPLOAD_DELAY", "0.5"))

notion = Client(auth=NOTION_TOKEN)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s',
    handlers=[
        logging.FileHandler("logs/notion_upload.log"),
        logging.StreamHandler()
    ]
)

# ---------------------- 유틸: Notion rich_text 제한 처리 ----------------------
def truncate_text(text, max_length=2000):
    return text if len(text) <= max_length else text[:max_length]

# ---------------------- 중복 키워드 확인 함수 ----------------------
def page_exists(keyword):
    query, error = call_with_backoff(
        notion.databases.query,
        database_id=NOTION_HOOK_DB_ID,
        filter={"property": "키워드", "title": {"equals": keyword}},
        page_size=1,
        logger=logging.getLogger(__name__)
    )
    if error:
        logging.warning(f"⚠️ 중복 확인 실패: {keyword} - {error}")
        return False
    return len(query.get("results", [])) > 0

# ---------------------- GPT 결과 파싱 함수 ----------------------
def parse_generated_text(text):
    hook_lines = re.findall(r"후킹 ?문장[0-9]?[\s:：\-\)]*([^\n]+)", text)
    blog_match = re.search(r"블로그(?:\s*초안)?[\s:：\-\)]*(.*?)\n+\s*(.*?\n+.*?\n+.*?)(?:\n|$)", text, re.DOTALL)
    video_titles = re.findall(r"(?:영상 제목|YouTube 제목)[\s:：\-\)]*[^\n]*\n?-\s*(.+)", text)

    blog_paragraphs = [p.strip() for p in blog_match[1].strip().split('\n')[:3]] if blog_match else ["", "", ""]
    return {
        "hook_lines": hook_lines[:2] if len(hook_lines) >= 2 else ["", ""],
        "blog_paragraphs": blog_paragraphs,
        "video_titles": video_titles[:2] if video_titles else ["", ""]
    }

# ---------------------- Notion 페이지 생성 함수 ----------------------
def create_notion_page(item):
    keyword = item["keyword"]
    parsed = parse_generated_text(item.get("generated_text", ""))
    topic = keyword.split()[0] if " " in keyword else keyword

    _, error = call_with_backoff(
        notion.pages.create,
        parent={"database_id": NOTION_HOOK_DB_ID},
        properties={
            "키워드": {"title": [{"text": {"content": keyword}}]},
            "채널": {"select": {"name": topic}},
            "등록일": {"date": {"start": datetime.utcnow().isoformat() + 'Z'}},
            "후킹문1": {"rich_text": [{"text": {"content": truncate_text(parsed["hook_lines"][0])}}]},
            "후킹문2": {"rich_text": [{"text": {"content": truncate_text(parsed["hook_lines"][1])}}]},
            "블로그초안": {"rich_text": [{"text": {"content": truncate_text('\n'.join(parsed["blog_paragraphs"]))}}]},
            "영상제목": {"rich_text": [{"text": {"content": truncate_text('\n'.join(parsed["video_titles"]))}}]}
        },
        logger=logging.getLogger(__name__)
    )
    return error

# ---------------------- 업로드 실행 함수 ----------------------
def upload_all_hooks():
    if not NOTION_TOKEN or not NOTION_HOOK_DB_ID:
        logging.error("❗ 환경 변수(NOTION_API_TOKEN, NOTION_HOOK_DB_ID)가 누락되었습니다.")
        return

    try:
        with open(HOOK_JSON_PATH, 'r', encoding='utf-8') as f:
            hooks = json.load(f)
    except Exception as e:
        logging.error(f"❗ 후킹 JSON 파일 읽기 오류: {e}")
        return

    total, success, skipped, failed = 0, 0, 0, 0
    failed_items = []

    for item in hooks:
        keyword = item.get("keyword")
        if not keyword:
            logging.warning("⛔ 빈 키워드 항목, 건너뜁니다.")
            continue

        total += 1
        if page_exists(keyword):
            logging.info(f"⏭️ 중복 스킵: {keyword}")
            skipped += 1
            continue

        error = create_notion_page(item)
        if not error:
            logging.info(f"✅ 업로드 완료: {keyword}")
            success += 1
        else:
            logging.error(f"❌ 업로드 실패: {keyword} - {error}")
            item["upload_error"] = error
            failed_items.append(item)
            failed += 1

        time.sleep(UPLOAD_DELAY)

    if failed_items:
        os.makedirs(os.path.dirname(FAILED_OUTPUT_PATH), exist_ok=True)
        with open(FAILED_OUTPUT_PATH, 'w', encoding='utf-8') as f:
            json.dump(failed_items, f, ensure_ascii=False, indent=2)
        logging.info(f"❗ 실패 항목 저장됨: {FAILED_OUTPUT_PATH}")

    logging.info("📊 후킹 업로드 요약")
    logging.info(f"총 항목: {total} | 성공: {success} | 중복스킵: {skipped} | 실패: {failed}")

if __name__ == "__main__":
    upload_all_hooks()
