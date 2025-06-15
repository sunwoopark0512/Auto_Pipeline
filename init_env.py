from dotenv import load_dotenv
import os


def load_env() -> dict:
    load_dotenv()

    env = {
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
        "NOTION_TOKEN": os.getenv("NOTION_TOKEN"),
        "SUPABASE_URL": os.getenv("SUPABASE_URL"),
        "SUPABASE_KEY": os.getenv("SUPABASE_KEY"),
        "SLACK_WEBHOOK": os.getenv("SLACK_WEBHOOK"),
        "WORDPRESS_API_TOKEN": os.getenv("WORDPRESS_API_TOKEN"),
    }
    return env
