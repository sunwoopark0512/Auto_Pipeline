"""Optimize generated text with grammar correction and basic SEO checks."""
import os
import json
import logging
from typing import List, Dict
from dotenv import load_dotenv
from language_tool_python import LanguageTool

# ---------------------- 환경 변수 및 기본값 로딩 ----------------------
load_dotenv()
INPUT_PATH = os.getenv("HOOK_INPUT_PATH", "data/generated_hooks.json")
OUTPUT_PATH = os.getenv("OPTIMIZED_HOOK_PATH", "data/optimized_hooks.json")
LANGUAGE = os.getenv("OPTIMIZE_LANG", "ko")

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

# ---------------------- 문법 및 SEO 점검 함수 ----------------------

def optimize_text(text: str, tool: LanguageTool) -> str:
    """Apply grammar corrections using LanguageTool."""
    if not text:
        return text
    matches = tool.check(text)
    return tool.correct(text, matches)


def keyword_in_text(keyword: str, text: str) -> bool:
    """Check if keyword appears in text (case-insensitive)."""
    if not keyword or not text:
        return False
    return keyword.lower() in text.lower()


def process_item(item: Dict, tool: LanguageTool) -> Dict:
    """Optimize texts and perform SEO checks."""
    keyword = item.get("keyword", "")
    optimized = item.copy()

    # Optimize hook lines and blog paragraphs if present
    hook_lines = item.get("hook_lines", [])
    optimized["hook_lines"] = [optimize_text(line, tool) for line in hook_lines]

    blog_paragraphs = item.get("blog_paragraphs", [])
    optimized["blog_paragraphs"] = [optimize_text(p, tool) for p in blog_paragraphs]

    # Simple SEO check: ensure keyword appears at least once
    seo_flags: List[str] = []
    for text in optimized.get("blog_paragraphs", []) + optimized.get("hook_lines", []):
        if not keyword_in_text(keyword, text):
            seo_flags.append(text)
    if seo_flags:
        optimized["seo_warning"] = f"Keyword '{keyword}' not found in some texts"
    return optimized

# ---------------------- 메인 실행 함수 ----------------------

def optimize_hooks() -> None:
    """Load hooks, run optimizations, and write the result file."""
    if not os.path.exists(INPUT_PATH):
        logging.error(f"Input file not found: {INPUT_PATH}")
        return

    try:
        with open(INPUT_PATH, "r", encoding="utf-8") as f:
            items = json.load(f)
    except Exception as e:
        logging.error(f"Failed to read input JSON: {e}")
        return

    if not isinstance(items, list):
        logging.error("Input JSON must be a list of hook objects")
        return

    tool = LanguageTool(f"{LANGUAGE}-KR" if LANGUAGE.startswith("ko") else LANGUAGE)
    optimized_items = [process_item(item, tool) for item in items]

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(optimized_items, f, ensure_ascii=False, indent=2)
    logging.info(f"Optimization complete. Results saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    optimize_hooks()
