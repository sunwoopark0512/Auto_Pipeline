import os
import json
import logging
from datetime import datetime
import requests
from dotenv import load_dotenv

load_dotenv()

WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
SUMMARY_PATH = os.getenv("REPARSED_OUTPUT_PATH", "logs/failed_keywords_reparsed.json")

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')


def build_summary():
    stats = {
        "total": 0,
        "failed": 0,
        "success": 0,
    }
    if os.path.exists(SUMMARY_PATH):
        try:
            with open(SUMMARY_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
            stats["total"] = len(data)
            stats["failed"] = len([d for d in data if d.get("retry_error")])
            stats["success"] = stats["total"] - stats["failed"]
        except Exception as e:
            logging.warning(f"Failed to parse summary file: {e}")
    return stats


def send_slack_message(webhook_url, message):
    if not webhook_url:
        logging.error("SLACK_WEBHOOK_URL is not set")
        return False
    try:
        response = requests.post(webhook_url, json={"text": message})
        if response.status_code != 200:
            logging.error(f"Slack API responded with status {response.status_code}: {response.text}")
            return False
        logging.info("Slack notification sent")
        return True
    except Exception as e:
        logging.error(f"Failed to send Slack notification: {e}")
        return False


if __name__ == "__main__":
    stats = build_summary()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    message = (
        f"Notion Hook pipeline finished at {timestamp}\n"
        f"Success: {stats['success']} / {stats['total']}\n"
        f"Failed: {stats['failed']}"
    )
    send_slack_message(WEBHOOK_URL, message)
