class SlackAlert:
    """Slack webhook alert helper."""

    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def send(self, message: str):
        """Mock sending Slack message."""
        print(f"Sending to Slack: {message}")
