import json
import logging
import os
import urllib.request
from typing import List, Dict, Optional

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')


def _send_slack(message: str, webhook_url: Optional[str]) -> None:
    if not webhook_url:
        logging.warning("⚠️ SLACK_WEBHOOK_URL 미설정")
        return
    data = json.dumps({"text": message}).encode("utf-8")
    req = urllib.request.Request(webhook_url, data=data, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as resp:
            logging.info(f"✅ Slack 전송 완료 (status={resp.status})")
    except Exception as exc:
        logging.error(f"❌ Slack 전송 실패: {exc}")


def notify(summary_path: Optional[str] = None, webhook_url: Optional[str] = None) -> None:
    summary_path = summary_path or os.getenv("REPARSED_OUTPUT_PATH", "logs/failed_keywords_reparsed.json")
    webhook_url = webhook_url or os.getenv("SLACK_WEBHOOK_URL")
    assert summary_path is not None

    if not os.path.exists(summary_path):
        logging.info(f"❗ 요약 파일이 존재하지 않습니다: {summary_path}")
        return

    with open(summary_path, "r", encoding="utf-8") as f:
        items: List[Dict] = json.load(f)

    total = len(items)
    failed = len([i for i in items if i.get("retry_error")])
    success = total - failed
    message = f"Retry Upload Result - Success: {success}, Failed: {failed}"
    logging.info(message)
    _send_slack(message, webhook_url)


if __name__ == "__main__":
    notify()
