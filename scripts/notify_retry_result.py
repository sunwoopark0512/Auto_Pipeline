import os
import json
import logging
from datetime import datetime
from dotenv import load_dotenv
import requests

load_dotenv()
REPARSED_OUTPUT_PATH = os.getenv("REPARSED_OUTPUT_PATH", "logs/failed_keywords_reparsed.json")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')


def summarize_results(items):
    total = len(items)
    failed = len([i for i in items if i.get("retry_error")])
    success = total - failed
    return total, success, failed


def send_slack_notification(message: str) -> None:
    if not SLACK_WEBHOOK_URL:
        logging.info("ℹ️ SLACK_WEBHOOK_URL not set; skipping Slack notification")
        return
    try:
        resp = requests.post(SLACK_WEBHOOK_URL, json={"text": message}, timeout=10)
        if resp.status_code != 200:
            raise RuntimeError(f"status {resp.status_code}: {resp.text}")
    except Exception as e:
        logging.error(f"❌ Failed to send Slack message: {e}")
        raise


def main():
    if not os.path.exists(REPARSED_OUTPUT_PATH):
        logging.info(f"✅ No retry results to notify: {REPARSED_OUTPUT_PATH} not found")
        return
    with open(REPARSED_OUTPUT_PATH, 'r', encoding='utf-8') as f:
        items = json.load(f)
    total, success, failed = summarize_results(items)
    msg = f"Retry Summary {datetime.now().strftime('%Y-%m-%d %H:%M')}: success {success}/{total}, failed {failed}"
    logging.info(msg)
    send_slack_notification(msg)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        exit(1)

