import os
from dotenv import load_dotenv


def load_env():
    """Load environment variables and return as dict."""
    load_dotenv()
    return {
        "NOTION_TOKEN": os.getenv("NOTION_TOKEN", ""),
        "WORDPRESS_API_TOKEN": os.getenv("WORDPRESS_API_TOKEN", ""),
        "SLACK_WEBHOOK": os.getenv("SLACK_WEBHOOK", ""),
    }
