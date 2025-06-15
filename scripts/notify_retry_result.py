import os
import json
import logging
from datetime import datetime
from dotenv import load_dotenv
import requests

# ---------------------- 설정 로딩 ----------------------
load_dotenv()
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
SUMMARY_PATH = os.getenv("REPARSED_OUTPUT_PATH", "logs/failed_keywords_reparsed.json")

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

# ---------------------- 데이터 로딩 ----------------------
def load_retry_data():
    if not os.path.exists(SUMMARY_PATH):
        logging.warning(f"❗ 요약 파일이 존재하지 않습니다: {SUMMARY_PATH}")
        return []
    with open(SUMMARY_PATH, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError as e:
            logging.error(f"❌ JSON 파싱 실패: {e}")
            return []

# ---------------------- 통계 계산 ----------------------
def summarize(data):
    total = len(data)
    failed = len([d for d in data if d.get("retry_error")])
    success = total - failed
    rate = round((success / total) * 100, 1) if total > 0 else 0.0
    return {
        "total": total,
        "success": success,
        "failed": failed,
        "rate": rate,
    }

# ---------------------- Slack 전송 ----------------------
def send_slack_message(message):
    if not SLACK_WEBHOOK_URL:
        logging.error("❌ SLACK_WEBHOOK_URL 환경 변수가 설정되지 않았습니다")
        return False
    try:
        response = requests.post(SLACK_WEBHOOK_URL, json={"text": message}, timeout=10)
        response.raise_for_status()
        logging.info("📣 Slack 알림 전송 성공")
        return True
    except Exception as e:
        logging.error(f"❌ Slack 알림 전송 실패: {e}")
        return False

# ---------------------- 실행 함수 ----------------------
def notify_retry_result():
    data = load_retry_data()
    stats = summarize(data)
    logging.info(f"📊 재시도 결과 요약: {stats}")

    message = (
        f"*Retry Result {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n"
        f"Total: {stats['total']}\n"
        f"Success: {stats['success']}\n"
        f"Failed: {stats['failed']}\n"
        f"Success Rate: {stats['rate']}%"
    )

    send_slack_message(message)

if __name__ == "__main__":
    notify_retry_result()
