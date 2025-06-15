"""Utility to filter generated hooks for banned words and quality issues."""

import json
import logging
import os
from typing import Dict, List, Tuple

BANNED_WORDS_PATH = os.getenv("BANNED_WORDS_PATH", "config/banned_words.txt")
INPUT_PATH = os.getenv("HOOK_OUTPUT_PATH", "data/generated_hooks.json")
OUTPUT_PATH = os.getenv("QA_OUTPUT_PATH", "data/qa_filtered_hooks.json")
FLAGGED_PATH = os.getenv("QA_FLAGGED_PATH", "logs/qa_flagged_hooks.json")

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

def load_banned_words(path: str) -> List[str]:
    """Return banned words from file if it exists."""

    if not os.path.exists(path):
        logging.warning("Banned words file not found: %s", path)
        return []
    with open(path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file if line.strip()]

def contains_banned_word(text: str, banned: List[str]) -> bool:
    """Return True if any banned word is present in ``text``."""

    lower_text = text.lower()
    return any(word.lower() in lower_text for word in banned)

def qa_filter(
    items: List[Dict[str, str]], banned: List[str]
) -> Tuple[List[Dict[str, str]], List[Dict[str, str]]]:
    """Split items into those that pass QA and those that fail."""

    passed: List[Dict[str, str]] = []
    flagged: List[Dict[str, str]] = []
    for item in items:
        content = "\n".join(
            item.get(field, "") if isinstance(item.get(field), str) else "\n".join(
                item.get(field, [])
            )
            for field in ["hook_lines", "blog_paragraphs", "video_titles", "generated_text"]
        )
        if not content.strip():
            item["qa_issue"] = "empty_content"
            flagged.append(item)
            continue
        if contains_banned_word(content, banned):
            item["qa_issue"] = "banned_word"
            flagged.append(item)
            continue
        passed.append(item)
    return passed, flagged

def run_qa_filter() -> None:
    """Entry point when executing as a script."""

    if not os.path.exists(INPUT_PATH):
        logging.error("Input file not found: %s", INPUT_PATH)
        return
    with open(INPUT_PATH, "r", encoding="utf-8") as file:
        items = json.load(file)
    banned = load_banned_words(BANNED_WORDS_PATH)
    passed, flagged = qa_filter(items, banned)

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as file:
        json.dump(passed, file, ensure_ascii=False, indent=2)
    if flagged:
        os.makedirs(os.path.dirname(FLAGGED_PATH), exist_ok=True)
        with open(FLAGGED_PATH, "w", encoding="utf-8") as file:
            json.dump(flagged, file, ensure_ascii=False, indent=2)
    logging.info("QA filter complete. passed=%d flagged=%d", len(passed), len(flagged))

if __name__ == "__main__":
    run_qa_filter()
