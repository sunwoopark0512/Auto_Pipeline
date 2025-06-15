from keyword_generator import generate_keywords
from content_writer import generate_article
from editor_seo_optimizer import optimize_text
from qa_filter import content_safety_check
from hook_uploader import upload_to_wordpress


def run_pipeline(topic: str, token: str) -> None:
    """Run the content generation pipeline for a given topic."""
    keywords = generate_keywords(topic)
    for keyword in keywords:
        draft = generate_article(keyword)
        revised = optimize_text(draft)
        if content_safety_check(revised):
            status, _ = upload_to_wordpress(
                title=keyword,
                content=revised,
                slug=keyword.replace(" ", "-"),
                token=token,
            )
            print(f"✅ Uploaded '{keyword}' with status {status}")
        else:
            print(f"⚠️ Content rejected for: {keyword}")
