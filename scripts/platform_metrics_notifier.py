import os
import json
import logging
from datetime import datetime
from notion_client import Client
from dotenv import load_dotenv

# ---------------------- 설정 로딩 ----------------------
load_dotenv()
NOTION_TOKEN = os.getenv("NOTION_API_TOKEN")
NOTION_REVENUE_DB_ID = os.getenv("NOTION_REVENUE_DB_ID")
METRICS_JSON_PATH = os.getenv("PLATFORM_METRICS_PATH", "data/platform_metrics.json")

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

if not NOTION_TOKEN or not NOTION_REVENUE_DB_ID:
    logging.error("❗ 환경 변수(NOTION_API_TOKEN, NOTION_REVENUE_DB_ID)가 누락되었습니다.")
    exit(1)

notion = Client(auth=NOTION_TOKEN)

# ---------------------- 메트릭 로드 ----------------------
def load_metrics():
    if not os.path.exists(METRICS_JSON_PATH):
        logging.error(f"❌ 메트릭 파일이 없습니다: {METRICS_JSON_PATH}")
        return [], None
    with open(METRICS_JSON_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    timestamp = data.get("timestamp")
    ts = datetime.fromisoformat(timestamp.replace('Z', '')) if timestamp else datetime.utcnow()
    return data.get("platforms", []), ts

# ---------------------- Notion 업로드 ----------------------
def push_metric(entry, ts):
    clicks = entry.get("clicks", 0)
    conversions = entry.get("conversions", 0)
    rate = round((conversions / clicks) * 100, 2) if clicks else 0.0
    try:
        notion.pages.create(
            parent={"database_id": NOTION_REVENUE_DB_ID},
            properties={
                "날짜": {"date": {"start": ts.isoformat() + 'Z'}},
                "플랫폼": {"title": [{"text": {"content": entry.get("name", "")}}]},
                "조회수": {"number": entry.get("views", 0)},
                "클릭수": {"number": clicks},
                "전환수": {"number": conversions},
                "전환율(%)": {"number": rate},
                "수익": {"number": entry.get("revenue", 0)}
            }
        )
        logging.info(f"✅ KPI 전송 완료: {entry.get('name')}")
    except Exception as e:
        logging.error(f"❌ KPI 전송 실패: {entry.get('name')} - {e}")

# ---------------------- 메인 실행 ----------------------
def upload_metrics():
    metrics, ts = load_metrics()
    if not metrics:
        logging.warning("📭 업로드할 메트릭이 없습니다.")
        return

    top = max(metrics, key=lambda x: x.get("revenue", 0))
    for m in metrics:
        push_metric(m, ts)

    logging.info(f"🏆 최고 수익 채널: {top.get('name')} 수익={top.get('revenue')}")

if __name__ == "__main__":
    upload_metrics()
