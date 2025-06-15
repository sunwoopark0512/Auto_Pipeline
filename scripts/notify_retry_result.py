import os
import json
import logging
import requests
from dotenv import load_dotenv

load_dotenv()
SUMMARY_PATH = os.getenv("REPARSED_OUTPUT_PATH", "logs/failed_keywords_reparsed.json")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

def load_summary():
    if not os.path.exists(SUMMARY_PATH):
        logging.error(f"❌ 요약 파일이 없습니다: {SUMMARY_PATH}")
        return None
    with open(SUMMARY_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    total = len(data)
    failed = len([d for d in data if d.get("retry_error")])
    success = total - failed
    return {"total": total, "success": success, "failed": failed}

def notify(summary):
    if not SLACK_WEBHOOK_URL:
        logging.error("❗ SLACK_WEBHOOK_URL 환경 변수가 설정되지 않았습니다.")
        return
    text = f"재업로드 결과 - 전체:{summary['total']} 성공:{summary['success']} 실패:{summary['failed']}"
    try:
        requests.post(SLACK_WEBHOOK_URL, json={"text": text})
        logging.info("📢 Slack 알림 전송 완료")
    except Exception as e:
        logging.error(f"Slack 전송 실패: {e}")

if __name__ == "__main__":
    s = load_summary()
    if s:
        notify(s)
