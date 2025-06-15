import logging

def send_slack_message(webhook: str, message: str) -> None:
    """Stub Slack notifier."""
    logging.info("SLACK: %s", message)
