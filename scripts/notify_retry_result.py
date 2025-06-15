"""Send Slack notifications about retry upload results."""

import json
import logging
import os
import requests

FAILED_PATH = os.getenv("REPARSED_OUTPUT_PATH", "logs/failed_keywords_reparsed.json")
WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s:%(message)s",
)


def send_slack_message(text: str) -> None:
    """Post a simple text message to the configured Slack webhook."""

    if not WEBHOOK_URL:
        logging.error("\u274c SLACK_WEBHOOK_URL 환경 변수가 설정되지 않았습니다.")
        return

    try:
        resp = requests.post(WEBHOOK_URL, json={"text": text}, timeout=10)
        if resp.status_code == 200:
            logging.info("\u2705 Slack 알림 전송 완료")
        else:
            logging.error(
                "\u274c Slack 전송 실패: %s %s", resp.status_code, resp.text
            )
    except requests.RequestException as exc:
        logging.error("\u274c Slack 전송 예외: %s", exc)


def notify_retry_result() -> None:
    """Read retry results and notify via Slack."""

    if not os.path.exists(FAILED_PATH):
        send_slack_message("✅ 모든 항목이 성공적으로 업로드되었습니다.")
        return

    with open(FAILED_PATH, 'r', encoding='utf-8') as f:
        items = json.load(f)

    if not items:
        send_slack_message("✅ 모든 항목이 성공적으로 업로드되었습니다.")
    else:
        keywords = [item.get("keyword", "") for item in items]
        message = f"❌ {len(keywords)}개 항목 업로드 실패\n" + ", ".join(keywords)
        send_slack_message(message)


if __name__ == "__main__":
    notify_retry_result()
