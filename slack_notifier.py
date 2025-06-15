"""Simple Slack notification utility using incoming webhooks."""

import os
import json
import logging
from urllib import request

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s'
)

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")


def send_slack_message(text: str, webhook_url: str | None = SLACK_WEBHOOK_URL) -> bool:
    """Send a Slack message using an incoming webhook."""
    if not webhook_url:
        logging.error("❗ SLACK_WEBHOOK_URL 환경변수가 설정되지 않았습니다.")
        return False

    data = json.dumps({"text": text}).encode("utf-8")
    req = request.Request(
        webhook_url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with request.urlopen(req) as resp:  # type: ignore[call-arg]
            if resp.status == 200:
                logging.info("✅ Slack 알림 전송 완료")
                return True
            logging.error("❌ Slack 전송 실패: %s", resp.read().decode("utf-8"))
            return False
    except Exception as exc:  # pylint: disable=broad-except
        logging.error("❌ Slack 전송 중 예외 발생: %s", exc)
        return False


if __name__ == "__main__":
    import sys

    message = sys.argv[1] if len(sys.argv) > 1 else "테스트 메시지"
    send_slack_message(message)
