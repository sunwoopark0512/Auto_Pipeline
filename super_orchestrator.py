"""High-level orchestration of the content generation pipeline."""

import time
from utils.init_env import load_env
from modules.keyword_generator import generate_keywords
from modules.content_writer import generate_article
from modules.editor_seo_optimizer import optimize_text
from modules.qa_filter import content_safety_check
from modules.hook_uploader import upload_to_wordpress
from modules.slack_notifier import send_slack_message
from modules.notion_sync import update_notion_status


env = load_env()


def run_pipeline(topic: str, token: str):
    """Run the full content generation and publishing pipeline."""

    keywords = generate_keywords(topic)
    for keyword in keywords:
        draft = generate_article(keyword)
        revised = optimize_text(draft)
        if content_safety_check(revised):
            _, _ = upload_to_wordpress(
                title=keyword, content=revised, slug=keyword.replace(" ", "-"), token=token
            )
            update_notion_status(env["NOTION_TOKEN"], keyword, "Published")
            send_slack_message(env["SLACK_WEBHOOK"], f"✅ Published: {keyword}")
        else:
            send_slack_message(env["SLACK_WEBHOOK"], f"❌ QA Rejected: {keyword}")
        time.sleep(1)
