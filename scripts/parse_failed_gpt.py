"""Parse GPT outputs from failed hook generation attempts."""

import os
import json
import logging
from dotenv import load_dotenv

load_dotenv()
FAILED_HOOK_PATH = os.getenv("FAILED_HOOK_PATH", "logs/failed_hooks.json")
REPARSED_OUTPUT_PATH = os.getenv("REPARSED_OUTPUT_PATH", "logs/failed_keywords_reparsed.json")

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

def parse_gpt_text(text: str):
    """Split raw GPT text into hook lines, blog paragraphs and video titles."""
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    hook_lines = lines[0:2]
    blog_paragraphs = lines[2:5]
    video_titles = lines[5:]
    return {
        "hook_lines": hook_lines,
        "blog_paragraphs": blog_paragraphs,
        "video_titles": video_titles,
    }

def parse_failed_gpt():
    """Parse all failed hook entries and write the cleaned file."""
    if not os.path.exists(FAILED_HOOK_PATH):
        logging.error("❌ 실패 후킹 파일이 없습니다: %s", FAILED_HOOK_PATH)
        return []

    with open(FAILED_HOOK_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    parsed = []
    for item in data:
        keyword = item.get("keyword")
        text = item.get("generated_text")
        if text:
            parsed_item = parse_gpt_text(text)
        else:
            parsed_item = {
                "hook_lines": item.get("hook_lines", ["", ""]),
                "blog_paragraphs": item.get("blog_paragraphs", ["", "", ""]),
                "video_titles": item.get("video_titles", ["", ""]),
            }
        parsed.append({"keyword": keyword, **parsed_item})

    os.makedirs(os.path.dirname(REPARSED_OUTPUT_PATH), exist_ok=True)
    with open(REPARSED_OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(parsed, f, ensure_ascii=False, indent=2)
    logging.info("✅ 파싱된 실패 키워드 저장 완료: %s", REPARSED_OUTPUT_PATH)
    return parsed

if __name__ == "__main__":
    parse_failed_gpt()
