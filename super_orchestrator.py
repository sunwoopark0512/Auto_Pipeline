import os
import time
import psycopg2
from notion_client import Client

from utils.init_env import load_env
from keyword_generator import generate_keywords
from content_writer import generate_article
from editor_seo_optimizer import optimize_text
from qa_filter import content_safety_check
from hook_uploader import upload_to_wordpress
from slack_notifier import send_slack_message

# Load ENV
env = load_env()

# Notion Client
notion = Client(auth=env.get("NOTION_TOKEN"))

# Supabase Local (psycopg2 사용)
def get_connection():
    """Create a database connection if possible."""
    try:
        return psycopg2.connect(
            host=os.getenv("SUPABASE_HOST", "localhost"),
            port=os.getenv("SUPABASE_PORT", "5432"),
            dbname=os.getenv("SUPABASE_DB", "supabase"),
            user=os.getenv("SUPABASE_USER", "postgres"),
            password=os.getenv("SUPABASE_PASSWORD", "postgres"),
        )
    except Exception:  # pragma: no cover - fallback for tests
        return None

conn = get_connection()

def record_content(keyword: str, title: str, content: str, status: str) -> None:
    """Record generated content to Supabase if connection available."""
    if conn is None:
        return
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO content_tracker (keyword, title, content, status)
        VALUES (%s, %s, %s, %s)
        """,
        (keyword, title, content, status),
    )
    conn.commit()
    cursor.close()


def update_notion(keyword: str, status: str) -> None:
    """Placeholder for Notion integration."""
    print(f"\u2705 Notion 업데이트 - {keyword}: {status}")


def run_pipeline(topic: str) -> None:
    """Run full content generation pipeline for a given topic."""
    keywords = generate_keywords(topic)
    for keyword in keywords:
        draft = generate_article(keyword)
        revised = optimize_text(draft)

        if content_safety_check(revised):
            status, _ = upload_to_wordpress(
                title=keyword,
                content=revised,
                slug=keyword.replace(" ", "-"),
                token=env.get("WORDPRESS_API_TOKEN", ""),
            )
            record_content(keyword, keyword, revised, "published")
            update_notion(keyword, "published")
            send_slack_message(env.get("SLACK_WEBHOOK", ""), f"\u2705 Published: {keyword}")
            print(f"\u2705 Uploaded: {keyword}")
        else:
            record_content(keyword, keyword, revised, "rejected")
            send_slack_message(env.get("SLACK_WEBHOOK", ""), f"\u274C QA Rejected: {keyword}")
            print(f"\u274C QA Rejected: {keyword}")
        time.sleep(1)  # API rate control


if __name__ == "__main__":
    topic = input("Enter topic: ")
    run_pipeline(topic)
