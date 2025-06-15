"""Notify Slack about results of retrying failed uploads."""

import os
import json
import logging
import requests
from dotenv import load_dotenv

load_dotenv()
REPARSED_OUTPUT_PATH = os.getenv("REPARSED_OUTPUT_PATH", "logs/failed_keywords_reparsed.json")
FAILED_HOOK_PATH = os.getenv("FAILED_HOOK_PATH", "logs/failed_hooks.json")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

def count_results():
    """Return numbers of successful and failed retries."""
    original = []
    if os.path.exists(FAILED_HOOK_PATH):
        with open(FAILED_HOOK_PATH, "r", encoding="utf-8") as f:
            original = json.load(f)
    total = len(original)

    still_failed = []
    if os.path.exists(REPARSED_OUTPUT_PATH):
        with open(REPARSED_OUTPUT_PATH, "r", encoding="utf-8") as f:
            still_failed = json.load(f)
    failed = len(still_failed)
    success = total - failed if total >= failed else 0
    return success, failed

def send_slack_message(success: int, failed: int):
    """Send summary message to Slack."""
    if not SLACK_WEBHOOK_URL:
        logging.error("❗ SLACK_WEBHOOK_URL 환경 변수가 설정되지 않았습니다.")
        return
    message = f"재시도 결과\n성공: {success}건\n실패: {failed}건"
    try:
        response = requests.post(SLACK_WEBHOOK_URL, json={"text": message}, timeout=10)
        response.raise_for_status()
        logging.info("✅ Slack 알림 전송 완료")
    except Exception as e:
        logging.error("❌ Slack 알림 전송 실패: %s", e)


def notify_retry_result():
    """Main entry to summarize retry results and notify via Slack."""
    success, failed = count_results()
    logging.info("재시도 요약 - 성공: %s, 실패: %s", success, failed)
    send_slack_message(success, failed)
    return success, failed

if __name__ == "__main__":
    notify_retry_result()
