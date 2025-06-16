import os
import json
import time
import logging
from datetime import datetime
from notion_client import Client
from dotenv import load_dotenv
from utils.encryption_util import EncryptionUtil

# ---------------------- 설정 로딩 ----------------------
load_dotenv()
NOTION_TOKEN = os.getenv("NOTION_API_TOKEN")
NOTION_HOOK_DB_ID = os.getenv("NOTION_HOOK_DB_ID")
FAILED_PATH = os.getenv("FAILED_HOOK_PATH", "logs/failed_keywords.json")
RETRY_DELAY = float(os.getenv("RETRY_DELAY", "0.5"))

# optional encryption
try:
    encryption_util = EncryptionUtil()
    ENCRYPT_ENABLED = True
except Exception:
    encryption_util = None
    ENCRYPT_ENABLED = False

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

# ---------------------- Notion 클라이언트 ----------------------
if not NOTION_TOKEN or not NOTION_HOOK_DB_ID:
    logging.error("❗ 환경 변수(NOTION_API_TOKEN, NOTION_HOOK_DB_ID)가 누락되었습니다.")
    exit(1)
notion = Client(auth=NOTION_TOKEN)

# ---------------------- 유틸: rich_text 길이 제한 ----------------------
def truncate_text(text, max_length=2000):
    return text if len(text) <= max_length else text[:max_length]

# ---------------------- 실패 키워드 로딩 ----------------------
def load_failed_items():
    if not os.path.exists(FAILED_PATH):
        logging.warning(f"❗ 실패 항목 파일이 존재하지 않습니다: {FAILED_PATH}")
        return []
    mode = 'rb' if ENCRYPT_ENABLED else 'r'
    with open(FAILED_PATH, mode) as f:
        raw = f.read()
        if ENCRYPT_ENABLED:
            return json.loads(encryption_util.decrypt(raw).decode('utf-8'))
        if isinstance(raw, bytes):
            raw = raw.decode('utf-8')
        return json.loads(raw)

# ---------------------- Notion 페이지 재생성 ----------------------
def create_retry_page(item):
    keyword = item.get('keyword')
    if not keyword:
        raise ValueError("keyword 누락됨")

    topic = keyword.split()[0] if " " in keyword else keyword

    parsed = item.get("parsed") or {
        "hook_lines": item.get("hook_lines", ["", ""]),
        "blog_paragraphs": item.get("blog_paragraphs", ["", "", ""]),
        "video_titles": item.get("video_titles", ["", ""])
    }

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

# ---------------------- 실행 함수 ----------------------
def retry_failed_uploads():
    failed_items = load_failed_items()
    if not failed_items:
        logging.info("✅ 재시도할 실패 항목이 없습니다.")
        return

    success, failed = 0, 0
    still_failed = []

    for item in failed_items:
        keyword = item.get("keyword")
        if not keyword:
            logging.warning("⛔ keyword 누락 항목 건너뜀")
            continue
        try:
            create_retry_page(item)
            logging.info(f"✅ 재업로드 성공: {keyword}")
            success += 1
        except Exception as e:
            logging.error(f"❌ 재시도 실패: {keyword} - {e}")
            item["retry_error"] = str(e)
            still_failed.append(item)
            failed += 1
        time.sleep(RETRY_DELAY)

    # 실패 파일 덮어쓰기
    if still_failed:
        failed_bytes = json.dumps(still_failed, ensure_ascii=False, indent=2).encode('utf-8')
        mode = 'wb' if ENCRYPT_ENABLED else 'w'
        with open(FAILED_PATH, mode) as f:
            if ENCRYPT_ENABLED:
                f.write(encryption_util.encrypt(failed_bytes))
            else:
                f.write(failed_bytes if 'b' in mode else failed_bytes.decode('utf-8'))
        logging.warning(f"🔁 여전히 실패한 항목 {len(still_failed)}개가 남아 있습니다.")

    # 요약
    logging.info("📦 재시도 업로드 요약")
    logging.info(f"성공: {success} | 실패 유지: {failed}")

if __name__ == "__main__":
    retry_failed_uploads()
