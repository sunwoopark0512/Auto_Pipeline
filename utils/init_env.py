"""Environment loading utilities."""

import os
from dotenv import load_dotenv


def load_env():
    """Load environment variables from ``.env`` and return them as a dict."""

    load_dotenv()
    env = {
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
        "NOTION_TOKEN": os.getenv("NOTION_TOKEN"),
        "SUPABASE_URL": os.getenv("SUPABASE_URL"),
        "SUPABASE_KEY": os.getenv("SUPABASE_KEY"),
        "SLACK_WEBHOOK": os.getenv("SLACK_WEBHOOK"),
        "WORDPRESS_API_TOKEN": os.getenv("WORDPRESS_API_TOKEN"),
        "STRIPE_SECRET_KEY": os.getenv("STRIPE_SECRET_KEY"),
    }
    return env
