import os
import json
import time
import logging
import time
from prometheus_client import start_http_server, Summary, Counter
from datetime import datetime
from notion_client import Client
from dotenv import load_dotenv

# ---------------------- 설정 로딩 ----------------------
load_dotenv()
NOTION_TOKEN = os.getenv("NOTION_API_TOKEN")
NOTION_DB_ID = os.getenv("NOTION_DB_ID")
KEYWORD_JSON_PATH = os.getenv("KEYWORD_OUTPUT_PATH", "data/keyword_output_with_cpc.json")
UPLOAD_DELAY = float(os.getenv("UPLOAD_DELAY", "0.5"))
CACHE_PATH = os.getenv("UPLOADED_CACHE_PATH", "data/uploaded_keywords_cache.json")
FAILED_PATH = os.getenv("FAILED_UPLOADS_PATH", "logs/failed_uploads.json")

# ---------------------- 로깅 설정 ----------------------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s',
    handlers=[
        logging.FileHandler("logs/notion_uploader.log"),
        logging.StreamHandler()
    ]
)

# ---------------------- 외부 서비스 초기화 ----------------------
try:
    import sentry_sdk
    sentry_sdk.init(os.getenv("SENTRY_DSN", ""))
except Exception as e:
    logging.warning(f"Sentry init failed: {e}")
    sentry_sdk = None

# ---------------------- Prometheus 메트릭 설정 ----------------------
METRICS_PORT = int(os.getenv("METRICS_PORT", "8002"))
start_http_server(METRICS_PORT)
UPLOAD_DURATION = Summary('keyword_upload_seconds', 'Time spent uploading keyword')
UPLOAD_SUCCESS = Counter('keyword_upload_success_total', 'Keyword upload success count')
UPLOAD_FAILURE = Counter('keyword_upload_failure_total', 'Keyword upload failure count')

# ---------------------- Notion 클라이언트 ----------------------
notion = Client(auth=NOTION_TOKEN)

# ---------------------- 캐시 로딩 ----------------------
if os.path.exists(CACHE_PATH):
    with open(CACHE_PATH, 'r', encoding='utf-8') as f:
        uploaded_cache = set(json.load(f))
else:
    uploaded_cache = set()

failed_uploads = []

# ---------------------- 중복 키워드 확인 함수 ----------------------
def page_exists(keyword):
    if keyword in uploaded_cache:
        return True
    try:
        query = notion.databases.query(
            database_id=NOTION_DB_ID,
            filter={"property": "키워드", "title": {"equals": keyword}},
            page_size=1
        )
        return len(query.get("results", [])) > 0
    except Exception as e:
        logging.warning(f"⚠️ 중복 확인 실패: {keyword} - {e}")
        return False

# ---------------------- Notion 페이지 생성 함수 ----------------------
def create_notion_page(item):
    topic = item['keyword'].split()[0]  # 첫 단어를 주제 채널로 활용

    notion.pages.create(
        parent={"database_id": NOTION_DB_ID},
        properties={
            "키워드": {"title": [{"text": {"content": item['keyword']}}]},
            "출처": {"select": {"name": item['source']}},
            "채널": {"select": {"name": topic}},
            "검색량": {"number": item.get("score", 0)},
            "성장률": {"number": item.get("growth", 0)},
            "멘션수": {"number": item.get("mentions", 0)},
            "최대리트윗": {"number": item.get("top_retweet", 0)},
            "CPC(원)": {"number": item.get("cpc", 0)},
            "등록일": {"date": {"start": datetime.utcnow().isoformat() + 'Z'}}
        }
    )

# ---------------------- 업로드 메인 함수 ----------------------
def upload_all_keywords():
    if not NOTION_TOKEN or not NOTION_DB_ID:
        logging.error("❗ 환경 변수(NOTION_API_TOKEN, NOTION_DB_ID)가 누락되었습니다.")
        return

    try:
        with open(KEYWORD_JSON_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            keywords = data.get("filtered_keywords", [])
    except Exception as e:
        logging.error(f"❗ 키워드 파일 읽기 오류: {e}")
        if sentry_sdk:
            sentry_sdk.capture_exception(e)
        return

    total = len(keywords)
    success, skipped, failed = 0, 0, 0

    for item in keywords:
        keyword = item.get('keyword')
        if not keyword:
            logging.warning("⛔ 빈 키워드 항목 발견, 건너뜁니다.")
            continue

        if page_exists(keyword):
            logging.info(f"⏭️ 중복 스킵: {keyword}")
            skipped += 1
            continue

        start_time = time.time()
        for attempt in range(3):
            try:
                create_notion_page(item)
                uploaded_cache.add(keyword)
                logging.info(f"✅ 업로드 완료: {keyword}")
                success += 1
                UPLOAD_SUCCESS.inc()
                time.sleep(UPLOAD_DELAY)
                break
            except Exception as e:
                logging.warning(f"🔁 재시도 {attempt + 1}/3 - {keyword} | 오류: {e}")
                if sentry_sdk:
                    sentry_sdk.capture_exception(e)
                time.sleep(1)
        else:
            logging.error(f"❌ 업로드 실패: {keyword} | 데이터: {item}")
            UPLOAD_FAILURE.inc()
            failed_uploads.append(item)
            failed += 1
        duration = time.time() - start_time
        UPLOAD_DURATION.observe(duration)

    # 캐시 저장
    try:
        os.makedirs(os.path.dirname(CACHE_PATH), exist_ok=True)
        with open(CACHE_PATH, 'w', encoding='utf-8') as f:
            json.dump(list(uploaded_cache), f, ensure_ascii=False, indent=2)
        logging.info(f"📦 업로드 캐시 저장 완료: {CACHE_PATH}")
    except Exception as e:
        logging.warning(f"⚠️ 캐시 저장 실패: {e}")
        if sentry_sdk:
            sentry_sdk.capture_exception(e)

    # 실패 로그 저장
    if failed_uploads:
        try:
            os.makedirs(os.path.dirname(FAILED_PATH), exist_ok=True)
            with open(FAILED_PATH, 'w', encoding='utf-8') as f:
                json.dump(failed_uploads, f, ensure_ascii=False, indent=2)
            logging.info(f"❗ 실패 항목 기록 완료: {FAILED_PATH}")
        except Exception as e:
            logging.warning(f"⚠️ 실패 로그 저장 실패: {e}")
            if sentry_sdk:
                sentry_sdk.capture_exception(e)

    # ---------------------- 요약 결과 출력 ----------------------
    logging.info("🎯 업로드 완료 요약")
    logging.info(f"총 키워드: {total} | 성공: {success} | 중복스킵: {skipped} | 실패: {failed}")

# ---------------------- 메인 진입점 ----------------------
if __name__ == "__main__":
    try:
        upload_all_keywords()
    except Exception as e:
        if sentry_sdk:
            sentry_sdk.capture_exception(e)
        raise
