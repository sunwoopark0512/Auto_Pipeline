import logging
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

SLACK_TOKEN = "your-slack-token"
CHANNEL = "#pipeline-notifications"

client = WebClient(token=SLACK_TOKEN)


def send_slack_notification(message: str) -> None:
    """Send a message to a Slack channel."""
    try:
        response = client.chat_postMessage(channel=CHANNEL, text=message)
        logging.info("Slack notification sent: %s", response["message"]["text"])
    except SlackApiError as exc:
        logging.error("Error sending Slack message: %s", exc.response["error"])
