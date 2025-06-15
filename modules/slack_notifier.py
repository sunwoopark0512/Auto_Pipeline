import os
import logging
from typing import Optional

import requests

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')


def send_slack_message(message: str, webhook_url: Optional[str] = None) -> None:
    """Send a simple text message to Slack via webhook."""
    url = webhook_url or os.getenv("SLACK_WEBHOOK_URL")
    if not url:
        logging.warning("SLACK_WEBHOOK_URL not configured; skipping Slack notification")
        return
    try:
        response = requests.post(url, json={"text": message}, timeout=10)
        if response.status_code != 200:
            logging.error("Slack webhook failed: %s - %s", response.status_code, response.text)
    except Exception as err:  # noqa: broad-except
        logging.error("Slack notification error: %s", err)
