import os
import json
import time
import logging
import re
from datetime import datetime
import asyncio
from notion_client import Client
from dotenv import load_dotenv

# ---------------------- 설정 로딩 ----------------------
load_dotenv()
NOTION_TOKEN = os.getenv("NOTION_API_TOKEN")
NOTION_HOOK_DB_ID = os.getenv("NOTION_HOOK_DB_ID")
HOOK_JSON_PATH = os.getenv("HOOK_OUTPUT_PATH", "data/generated_hooks.json")
FAILED_OUTPUT_PATH = "data/upload_failed_hooks.json"
UPLOAD_DELAY = float(os.getenv("UPLOAD_DELAY", "0.5"))
CACHE_PATH = os.getenv("HOOK_CACHE_PATH", "data/uploaded_hooks_cache.json")
UPLOAD_WORKERS = int(os.getenv("UPLOAD_WORKERS", "5"))

notion = Client(auth=NOTION_TOKEN)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s',
    handlers=[
        logging.FileHandler("logs/notion_upload.log"),
        logging.StreamHandler()
    ]
)

# ---------------------- 캐시 로딩 ----------------------
if os.path.exists(CACHE_PATH):
    with open(CACHE_PATH, 'r', encoding='utf-8') as f:
        uploaded_cache = set(json.load(f))
else:
    uploaded_cache = set()

# ---------------------- 유틸: Notion rich_text 제한 처리 ----------------------
def truncate_text(text, max_length=2000):
    return text if len(text) <= max_length else text[:max_length]

# ---------------------- 중복 키워드 확인 함수 ----------------------
def _page_exists_sync(keyword):
    query = notion.databases.query(
        database_id=NOTION_HOOK_DB_ID,
        filter={"property": "키워드", "title": {"equals": keyword}},
        page_size=1
    )
    return len(query.get("results", [])) > 0

async def page_exists(keyword):
    if keyword in uploaded_cache:
        return True
    try:
        exists = await asyncio.to_thread(_page_exists_sync, keyword)
        if exists:
            uploaded_cache.add(keyword)
        return exists
    except Exception as e:
        logging.warning(f"⚠️ 중복 확인 실패: {keyword} - {e}")
        return False

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

    notion.pages.create(
        parent={"database_id": NOTION_HOOK_DB_ID},
        properties={
            "키워드": {"title": [{"text": {"content": keyword}}]},
            "채널": {"select": {"name": topic}},
            "등록일": {"date": {"start": datetime.utcnow().isoformat() + 'Z'}},
            "후킹문1": {"rich_text": [{"text": {"content": truncate_text(parsed["hook_lines"][0])}}]},
            "후킹문2": {"rich_text": [{"text": {"content": truncate_text(parsed["hook_lines"][1])}}]},
            "블로그초안": {"rich_text": [{"text": {"content": truncate_text('\n'.join(parsed["blog_paragraphs"]))}}]},
            "영상제목": {"rich_text": [{"text": {"content": truncate_text('\n'.join(parsed["video_titles"]))}}]}
        }
    )

async def create_notion_page_async(item):
    await asyncio.to_thread(create_notion_page, item)

# ---------------------- 업로드 실행 함수 ----------------------
async def upload_all_hooks():
    if not NOTION_TOKEN or not NOTION_HOOK_DB_ID:
        logging.error("❗ 환경 변수(NOTION_API_TOKEN, NOTION_HOOK_DB_ID)가 누락되었습니다.")
        return

    try:
        with open(HOOK_JSON_PATH, 'r', encoding='utf-8') as f:
            hooks = json.load(f)
    except Exception as e:
        logging.error(f"❗ 후킹 JSON 파일 읽기 오류: {e}")
        return

    sem = asyncio.Semaphore(UPLOAD_WORKERS)
    results = []

    async def process_item(item):
        keyword = item.get("keyword")
        if not keyword:
            logging.warning("⛔ 빈 키워드 항목, 건너뜁니다.")
            return "skip", None

        async with sem:
            if await page_exists(keyword):
                logging.info(f"⏭️ 중복 스킵: {keyword}")
                await asyncio.sleep(UPLOAD_DELAY)
                return "skip", None

            for attempt in range(3):
                try:
                    await create_notion_page_async(item)
                    uploaded_cache.add(keyword)
                    logging.info(f"✅ 업로드 완료: {keyword}")
                    await asyncio.sleep(UPLOAD_DELAY)
                    return "success", None
                except Exception as e:
                    logging.warning(f"🔁 재시도 {attempt+1}/3 - {keyword} | 오류: {e}")
                    await asyncio.sleep(1)

            logging.error(f"❌ 업로드 실패: {keyword}")
            await asyncio.sleep(UPLOAD_DELAY)
            return "failed", item

    tasks = [process_item(item) for item in hooks]
    results = await asyncio.gather(*tasks)

    total = len(hooks)
    success = sum(1 for r, _ in results if r == "success")
    skipped = sum(1 for r, _ in results if r == "skip")
    failed_items = [item for r, item in results if r == "failed"]
    failed = len(failed_items)

    if failed_items:
        os.makedirs(os.path.dirname(FAILED_OUTPUT_PATH), exist_ok=True)
        with open(FAILED_OUTPUT_PATH, 'w', encoding='utf-8') as f:
            json.dump(failed_items, f, ensure_ascii=False, indent=2)
        logging.info(f"❗ 실패 항목 저장됨: {FAILED_OUTPUT_PATH}")

    if uploaded_cache:
        os.makedirs(os.path.dirname(CACHE_PATH), exist_ok=True)
        with open(CACHE_PATH, 'w', encoding='utf-8') as f:
            json.dump(list(uploaded_cache), f, ensure_ascii=False, indent=2)

    logging.info("📊 후킹 업로드 요약")
    logging.info(f"총 항목: {total} | 성공: {success} | 중복스킵: {skipped} | 실패: {failed}")

if __name__ == "__main__":
    asyncio.run(upload_all_hooks())
