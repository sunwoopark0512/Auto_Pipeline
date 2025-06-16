import os
import json
import logging
from datetime import datetime
from notion_client import Client
from dotenv import load_dotenv
from privacy_manager import request_data_deletion

# ---------------------- 설정 로딩 ----------------------
load_dotenv()
NOTION_TOKEN = os.getenv("NOTION_API_TOKEN")
NOTION_KPI_DB_ID = os.getenv("NOTION_KPI_DB_ID")
SUMMARY_PATH = os.getenv("REPARSED_OUTPUT_PATH", "logs/failed_keywords_reparsed.json")
DELETE_USER_ID = os.getenv("DELETE_USER_ID")

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

# ---------------------- 개인정보 삭제 처리 ----------------------
if DELETE_USER_ID:
    request_data_deletion(DELETE_USER_ID, SUMMARY_PATH)

# ---------------------- Notion 클라이언트 ----------------------
if not NOTION_TOKEN or not NOTION_KPI_DB_ID:
    logging.error("❗ 환경 변수(NOTION_API_TOKEN, NOTION_KPI_DB_ID)가 누락되었습니다.")
    exit(1)
notion = Client(auth=NOTION_TOKEN)

# ---------------------- KPI 데이터 수집 ----------------------
def get_retry_stats():
    if not os.path.exists(SUMMARY_PATH):
        logging.error(f"❌ 재시도 데이터 파일이 없습니다: {SUMMARY_PATH}")
        return None

    with open(SUMMARY_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    total = len(data)
    failed = len([d for d in data if d.get("retry_error")])
    success = total - failed
    rate = round((success / total) * 100, 1) if total > 0 else 0.0

    now = datetime.now()
    return {
        "date": now,
        "total": total,
        "success": success,
        "failed": failed,
        "rate": rate
    }

# ---------------------- Notion KPI 행 추가 ----------------------
def push_kpi_to_notion(kpi):
    try:
        notion.pages.create(
            parent={"database_id": NOTION_KPI_DB_ID},
            properties={
                "날짜": {"date": {"start": kpi["date"].isoformat()}},
                "전체 시도": {"number": kpi["total"]},
                "성공": {"number": kpi["success"]},
                "실패": {"number": kpi["failed"]},
                "성공률(%)": {"number": kpi["rate"]}
            }
        )
        logging.info("📊 Notion KPI 업데이트 완료")
    except Exception as e:
        logging.error(f"❌ Notion KPI 전송 실패: {e}")

# ---------------------- 실행 진입점 ----------------------
if __name__ == "__main__":
    kpi = get_retry_stats()
    if kpi:
        logging.info(f"📈 KPI 요약: {kpi}")
        push_kpi_to_notion(kpi)
