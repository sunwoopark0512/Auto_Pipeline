import os
import json
import logging
import requests
from datetime import datetime

# ---------------------- 환경 변수 로딩 ----------------------
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
SUMMARY_PATH = os.getenv("REPARSED_OUTPUT_PATH", "logs/failed_keywords_reparsed.json")

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

# ---------------------- 실패 데이터 로드 ----------------------
def load_retry_data():
    if not os.path.exists(SUMMARY_PATH):
        logging.warning(f"❗ 재시도 결과 파일이 존재하지 않습니다: {SUMMARY_PATH}")
        return []
    try:
        with open(SUMMARY_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"❌ 파일 로딩 실패: {e}")
        return []

# ---------------------- 요약 계산 ----------------------
def summarize_results(items):
    total = len(items)
    still_failed = len([it for it in items if it.get("retry_error")])
    succeeded = total - still_failed
    return {
        "total": total,
        "succeeded": succeeded,
        "still_failed": still_failed,
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M')
    }

# ---------------------- Slack 알림 전송 ----------------------
def send_slack_notification(summary):
    if not SLACK_WEBHOOK_URL:
        logging.error("❌ SLACK_WEBHOOK_URL 환경 변수가 설정되지 않았습니다.")
        return False

    message = (
        f"📦 Retry 결과 ({summary['timestamp']})\n"
        f"총 항목: {summary['total']}\n"
        f"성공: {summary['succeeded']}\n"
        f"실패 유지: {summary['still_failed']}"
    )

    try:
        response = requests.post(SLACK_WEBHOOK_URL, json={"text": message}, timeout=10)
        response.raise_for_status()
        logging.info("✅ Slack 알림 전송 완료")
        return True
    except Exception as e:
        logging.error(f"❌ Slack 알림 전송 실패: {e}")
        return False

# ---------------------- 메인 ----------------------
if __name__ == "__main__":
    data = load_retry_data()
    summary = summarize_results(data)
    logging.info(f"📈 재시도 요약: {summary}")
    send_slack_notification(summary)
