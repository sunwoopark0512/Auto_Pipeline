import os
import json
import logging
from datetime import datetime
from dotenv import load_dotenv
import requests

load_dotenv()
WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
RETRY_LOG_PATH = os.getenv("REPARSED_OUTPUT_PATH", "logs/failed_keywords_reparsed.json")

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')


def summarize() -> dict:
    if not os.path.exists(RETRY_LOG_PATH):
        logging.warning(f"재시도 로그 파일을 찾을 수 없습니다: {RETRY_LOG_PATH}")
        return {"total": 0, "success": 0, "failed": 0}

    with open(RETRY_LOG_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    total = len(data)
    failed = len([d for d in data if d.get("retry_error")])
    success = total - failed
    return {"total": total, "success": success, "failed": failed}


def send_notification(summary: dict) -> None:
    text = (
        f"🔄 Retry Upload Result ({datetime.utcnow().isoformat()} UTC)\n"
        f"Total: {summary['total']}\n"
        f"Success: {summary['success']}\n"
        f"Failed: {summary['failed']}"
    )
    if WEBHOOK_URL:
        try:
            requests.post(WEBHOOK_URL, json={"text": text})
            logging.info("📣 알림 전송 완료")
        except Exception as e:
            logging.error(f"알림 전송 실패: {e}")
    else:
        logging.info(text)


def main() -> None:
    summary = summarize()
    send_notification(summary)


if __name__ == "__main__":
    main()
