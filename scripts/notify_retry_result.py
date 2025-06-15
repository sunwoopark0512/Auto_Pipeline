import os
import json
import logging
from dotenv import load_dotenv

load_dotenv()

RESULT_PATH = os.getenv("REPARSED_OUTPUT_PATH", "logs/failed_keywords_reparsed.json")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')


def build_summary() -> str:
    if not os.path.exists(RESULT_PATH):
        return "No retry result file found."
    with open(RESULT_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    total = len(data)
    failed = len([d for d in data if d.get("retry_error")])
    success = total - failed
    return f"Retry summary - total: {total}, success: {success}, failed: {failed}"


def send_slack_message(message: str) -> None:
    if not SLACK_WEBHOOK_URL:
        logging.info(message)
        return
    try:
        import requests  # type: ignore

        response = requests.post(SLACK_WEBHOOK_URL, json={"text": message})
        if response.status_code != 200:
            logging.error(f"Slack notification failed: {response.text}")
    except Exception as e:
        logging.error(f"Slack notification error: {e}")


def main() -> None:
    summary = build_summary()
    send_slack_message(summary)


if __name__ == "__main__":
    main()
