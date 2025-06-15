"""Slack notification for retry results."""

import os
import json
import logging
import requests
from dotenv import load_dotenv

# ---------------------- 환경 변수 로딩 ----------------------
load_dotenv()
REPARSED_OUTPUT_PATH = os.getenv("REPARSED_OUTPUT_PATH", "logs/failed_keywords_reparsed.json")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

# ---------------------- 결과 파일 로딩 ----------------------
def load_retry_results():
    """Load parsed retry results from disk."""
    if not os.path.exists(REPARSED_OUTPUT_PATH):
        logging.error("❌ 결과 파일이 없습니다: %s", REPARSED_OUTPUT_PATH)
        return None
    try:
        with open(REPARSED_OUTPUT_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logging.error("❌ 결과 파일 읽기 오류: %s", e)
        return None

# ---------------------- Slack 알림 전송 ----------------------
def send_slack_notification(success: int, failed: int) -> bool:
    """Post the retry summary message to Slack."""
    if not SLACK_WEBHOOK_URL:
        logging.error("❗ SLACK_WEBHOOK_URL 환경 변수가 설정되지 않았습니다.")
        return False
    message = f"재시도 결과 보고\n성공: {success}개\n실패: {failed}개"
    try:
        response = requests.post(SLACK_WEBHOOK_URL, json={"text": message}, timeout=10)
        response.raise_for_status()
        logging.info("📨 Slack 알림 전송 성공")
        return True
    except Exception as e:
        logging.error("❌ Slack 알림 전송 실패: %s", e)
        return False

# ---------------------- 메인 진입점 ----------------------
def main():
    """Entry point for CLI execution."""
    results = load_retry_results()
    if results is None:
        return

    total = len(results)
    failed = len([r for r in results if r.get("retry_error")])
    success = total - failed

    logging.info("재시도 성공: %s | 여전히 실패: %s", success, failed)
    send_slack_notification(success, failed)

if __name__ == "__main__":
    main()
