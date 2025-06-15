import os
import logging
from dotenv import load_dotenv
import requests


def main():
    load_dotenv()
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')
    webhook = os.getenv("SLACK_WEBHOOK_URL")
    summary = os.getenv("REPARSED_OUTPUT_PATH", "logs/failed_keywords_reparsed.json")
    if not webhook:
        logging.warning("SLACK_WEBHOOK_URL not configured")
        return
    message = f"Retry summary available: {summary}"
    try:
        requests.post(webhook, json={"text": message})
        logging.info("Sent retry summary notification")
    except Exception as e:
        logging.error(f"Notification failed: {e}")


if __name__ == "__main__":
    main()
