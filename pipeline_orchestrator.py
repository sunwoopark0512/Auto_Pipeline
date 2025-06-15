from keyword_generator import generate_keywords
from content_writer import generate_article
from editor_seo_optimizer import optimize_text
from qa_filter import content_safety_check
from hook_uploader import upload_hook


def run_pipeline(topic: str, token: str) -> None:
    """Simple pipeline orchestrator used by dashboard."""
    keywords = generate_keywords(topic)
    article = generate_article(topic, 500)
    optimized = optimize_text(article)

    if not content_safety_check(optimized):
        raise ValueError("Generated content failed safety check")

    upload_hook({"topic": topic, "content": optimized, "token": token})
