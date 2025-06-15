"""Notify Slack of retry results."""

import json
import logging
import os
from typing import List, Dict, Any

from dotenv import load_dotenv
import requests

load_dotenv()
WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
SUMMARY_PATH = os.getenv("REPARSED_OUTPUT_PATH", "logs/failed_keywords_reparsed.json")

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s:%(message)s")


def load_summary() -> List[Dict[str, Any]]:
    """Load retry summary data from ``SUMMARY_PATH``."""
    if not os.path.exists(SUMMARY_PATH):
        logging.warning("❗ 결과 파일이 없습니다: %s", SUMMARY_PATH)
        return []
    with open(SUMMARY_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def send_slack_message(text: str) -> None:
    """Send ``text`` to Slack via incoming webhook."""
    if not WEBHOOK_URL:
        logging.error("❗ SLACK_WEBHOOK_URL 환경 변수가 설정되지 않았습니다.")
        return
    try:
        response = requests.post(WEBHOOK_URL, json={"text": text}, timeout=10)
        if response.status_code == 200:
            logging.info("✅ 슬랙 알림 전송 완료")
        else:
            logging.error("❌ 슬랙 전송 실패: %s %s", response.status_code, response.text)
    except Exception as exc:  # pylint: disable=broad-exception-caught
        logging.error("❌ 슬랙 요청 중 오류: %s", exc)


def notify_result() -> None:
    """Read retry results and send a Slack notification."""
    summary = load_summary()
    total = len(summary)
    failed = len([s for s in summary if s.get("retry_error")])
    success = total - failed

    message = (
        "📢 Notion 업로드 재시도 결과\n"
        f"총 항목: {total}\n"
        f"성공: {success}\n"
        f"실패: {failed}"
    )
    send_slack_message(message)


if __name__ == "__main__":
    notify_result()
