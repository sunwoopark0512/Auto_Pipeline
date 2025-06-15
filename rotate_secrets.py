import logging
import os
import requests
from random import random

from logging_config import setup_logging

setup_logging()

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")


def rotate_secrets():
    logging.info("Rotating secrets...")
    success = random() > 0.1  # placeholder for real rotation logic
    if success:
        logging.info("Secret rotation succeeded")
    else:
        logging.error("Secret rotation failed")
    return success


def notify_slack(success: bool):
    if not SLACK_WEBHOOK_URL:
        logging.warning("No Slack webhook configured")
        return
    message = {"text": f"rotate-secrets {'succeeded' if success else 'failed'}"}
    try:
        requests.post(SLACK_WEBHOOK_URL, json=message, timeout=5)
    except Exception as e:
        logging.warning("Slack notification failed: %s", e)


def main():
    success = rotate_secrets()
    notify_slack(success)
    if not success:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
