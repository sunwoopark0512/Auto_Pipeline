"""Parse failed GPT hook outputs to structured data."""

import os
import json
import logging
import re
from dotenv import load_dotenv

load_dotenv()

FAILED_HOOK_PATH = os.getenv("FAILED_HOOK_PATH", "logs/failed_hooks.json")
REPARSED_OUTPUT_PATH = os.getenv("REPARSED_OUTPUT_PATH", "logs/failed_keywords_reparsed.json")

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')


def parse_generated_text(text: str):
    """Extract hook lines, blog paragraphs and video titles from GPT text."""
    raw_lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    cleaned = [
        re.sub(
            r"^(후킹 ?문장\d*|블로그(?:\s*초안)?|영상 제목|YouTube 제목)\s*[:：\-\)]*",
            "",
            ln,
        ).strip()
        for ln in raw_lines
    ]
    cleaned = [ln for ln in cleaned if ln]

    hook_lines = cleaned[0:2]
    blog_paragraphs = cleaned[2:5]
    video_titles = cleaned[5:7]

    return {
        "hook_lines": hook_lines if len(hook_lines) == 2 else ["", ""],
        "blog_paragraphs": (blog_paragraphs + ["", "", ""])[:3],
        "video_titles": (video_titles + ["", ""])[:2],
    }


def parse_entry(entry: dict):
    """Parse a single failed hook entry."""
    text = entry.get("generated_text") or ""
    if text:
        parsed = parse_generated_text(text)
    else:
        parsed = {
            "hook_lines": entry.get("hook_lines", ["", ""]),
            "blog_paragraphs": entry.get("blog_paragraphs", ["", "", ""]),
            "video_titles": entry.get("video_titles", ["", ""]),
        }
    return {
        "keyword": entry.get("keyword", ""),
        "hook_lines": parsed.get("hook_lines", ["", ""]),
        "blog_paragraphs": parsed.get("blog_paragraphs", ["", "", ""]),
        "video_titles": parsed.get("video_titles", ["", ""]),
    }


def main():
    """Entry point for CLI usage."""
    if not os.path.exists(FAILED_HOOK_PATH):
        logging.error("❌ 실패 후킹 파일이 없습니다: %s", FAILED_HOOK_PATH)
        return

    with open(FAILED_HOOK_PATH, "r", encoding="utf-8") as f:
        failed_data = json.load(f)

    results = []
    for item in failed_data:
        keyword = item.get("keyword")
        if not keyword:
            logging.warning("⛔ keyword 누락 항목 건너뜀")
            continue
        parsed_item = parse_entry(item)
        results.append(parsed_item)
        logging.info("✅ 파싱 완료: %s", keyword)

    os.makedirs(os.path.dirname(REPARSED_OUTPUT_PATH), exist_ok=True)
    with open(REPARSED_OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    logging.info("🎉 파싱 결과 저장 완료: %s", REPARSED_OUTPUT_PATH)


if __name__ == "__main__":
    main()
