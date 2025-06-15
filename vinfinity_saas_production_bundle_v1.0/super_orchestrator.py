import time

from utils.init_env import load_env
from modules import (
    keyword_generator as kg,
    content_writer as cw,
    editor_seo_optimizer as eo,
    qa_filter as qf,
)
from modules.uploader_multi_platform import upload_all
from modules.slack_notifier import send_slack_message
from db_utils import record_content
from billing_utils import check_user_quota

env = load_env()


def run_pipeline(topic: str, token: str, user_id: str | None = None):
    if user_id:
        check_user_quota(user_id)

    keywords = kg.generate_keywords(topic)
    for kw in keywords:
        draft = cw.generate_article(kw)
        revised = eo.optimize_text(draft)

        if qf.content_safety_check(revised):
            upload_all(kw, revised, kw.replace(" ", "-"), token)
            status = "published"
            send_slack_message(env["SLACK_WEBHOOK"], f"✅ Published: {kw}")
        else:
            status = "rejected"
            send_slack_message(env["SLACK_WEBHOOK"], f"❌ QA Rejected: {kw}")

        if user_id:
            record_content(user_id, kw, revised, status)
        time.sleep(1)
