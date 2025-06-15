import os
import json
import logging

import requests
from dotenv import load_dotenv

# ---------------------- 설정 로딩 ----------------------
load_dotenv()
SUMMARY_PATH = os.getenv("REPARSED_OUTPUT_PATH", "logs/failed_keywords_reparsed.json")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s:%(message)s")


def load_retry_data():
    if not os.path.exists(SUMMARY_PATH):
        logging.error(f"❌ 재시도 결과 파일이 없습니다: {SUMMARY_PATH}")
        return None
    with open(SUMMARY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def count_results(data):
    total = len(data)
    failed = len([d for d in data if d.get("retry_error")])
    success = total - failed
    return total, success, failed


def send_slack_message(message: str) -> None:
    if not SLACK_WEBHOOK_URL:
        logging.error("❗ SLACK_WEBHOOK_URL 환경 변수가 설정되지 않았습니다.")
        return
    try:
        response = requests.post(SLACK_WEBHOOK_URL, json={"text": message}, timeout=10)
        response.raise_for_status()
        logging.info("📨 Slack 알림 전송 성공")
    except Exception as e:
        logging.error(f"❌ Slack 알림 전송 실패: {e}")


def main():
    data = load_retry_data()
    if data is None:
        send_slack_message(f"재시도 결과 파일을 찾을 수 없습니다: {SUMMARY_PATH}")
        return

    total, success, failed = count_results(data)
    message = f"재업로드 결과\n총 시도: {total}\n성공: {success}\n실패: {failed}"
    send_slack_message(message)


if __name__ == "__main__":
    main()
