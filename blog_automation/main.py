from .content_generator import generate_blog_post
from .quality_checker import grammar_check
from .seo_adaptor import fetch_latest_updates
from .system_resilience import backup_files
from .legal_compliance import detect_copyright


def run_blog_pipeline(topic: str, outline):
    """Example pipeline tying all modules together."""
    post = generate_blog_post(topic, outline)
    issues = grammar_check(post)
    seo_updates = fetch_latest_updates()
    backup_files(["data/generated_post.txt"])
    copyright_marks = detect_copyright(post)

    with open("data/generated_post.txt", "w", encoding="utf-8") as f:
        f.write(post)

    return {
        "issues": issues,
        "seo": seo_updates,
        "copyright": copyright_marks,
    }


if __name__ == "__main__":
    result = run_blog_pipeline("Travel Tips", ["packing", "budget", "safety"])
    print(result)
