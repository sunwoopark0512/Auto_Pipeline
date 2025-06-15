import os
import json
import logging
import urllib.request
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

REPARSED_PATH = os.getenv("REPARSED_OUTPUT_PATH", "logs/failed_keywords_reparsed.json")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')


def get_remaining_failures() -> int:
    if not os.path.exists(REPARSED_PATH):
        return 0
    with open(REPARSED_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return len(data)


def send_slack_message(message: str) -> None:
    if not SLACK_WEBHOOK_URL:
        logging.warning("SLACK_WEBHOOK_URL 미설정, 알림 생략")
        return
    payload = json.dumps({"text": message}).encode("utf-8")
    req = urllib.request.Request(
        SLACK_WEBHOOK_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req) as resp:
            resp.read()
        logging.info("Slack 알림 전송 완료")
    except Exception as e:
        logging.error(f"Slack 알림 실패: {e}")


def notify_retry_result() -> None:
    remaining = get_remaining_failures()
    msg = (
        f"재시도 완료 - 남은 실패 항목: {remaining}개"
        f" ({datetime.now().strftime('%Y-%m-%d %H:%M')})"
    )
    logging.info(msg)
    send_slack_message(msg)


if __name__ == "__main__":
    notify_retry_result()
