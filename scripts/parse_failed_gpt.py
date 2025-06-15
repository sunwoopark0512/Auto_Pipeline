import os
import json
import logging
from dotenv import load_dotenv

load_dotenv()

FAILED_HOOK_PATH = os.getenv("FAILED_HOOK_PATH", "logs/failed_hooks.json")
OUTPUT_PATH = os.getenv("REPARSED_OUTPUT_PATH", "logs/failed_keywords_reparsed.json")

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')


def simple_parse(text: str) -> dict:
    """Parse GPT output in a very naive way."""
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    hook_lines = lines[0:2]
    blog_paragraphs = lines[2:5]
    video_titles = lines[5:7]
    return {
        "hook_lines": hook_lines + ["", ""][:2-len(hook_lines)],
        "blog_paragraphs": blog_paragraphs + ["", "", ""][:3-len(blog_paragraphs)],
        "video_titles": video_titles + ["", ""][:2-len(video_titles)],
    }


def main() -> None:
    if not os.path.exists(FAILED_HOOK_PATH):
        logging.info(f"No failed hook file found at {FAILED_HOOK_PATH}")
        return

    with open(FAILED_HOOK_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    parsed_items = []
    for item in data:
        generated = item.get("generated_text", "")
        parsed = simple_parse(generated)
        item["parsed"] = parsed
        parsed_items.append(item)

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(parsed_items, f, ensure_ascii=False, indent=2)
    logging.info(f"Parsed results written to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
