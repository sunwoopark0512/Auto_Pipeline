import os
import json
import logging
from dotenv import load_dotenv
from notion_hook_uploader import parse_generated_text

load_dotenv()
FAILED_HOOK_PATH = os.getenv("FAILED_HOOK_PATH", "logs/failed_hooks.json")
REPARSED_OUTPUT_PATH = os.getenv("REPARSED_OUTPUT_PATH", "logs/failed_keywords_reparsed.json")

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')


def parse_failed_items():
    if not os.path.exists(FAILED_HOOK_PATH):
        logging.info(f"✅ No failed hooks to parse: {FAILED_HOOK_PATH} not found")
        return []
    try:
        with open(FAILED_HOOK_PATH, 'r', encoding='utf-8') as f:
            items = json.load(f)
    except Exception as e:
        logging.error(f"❌ Could not read {FAILED_HOOK_PATH}: {e}")
        raise

    parsed_items = []
    for item in items:
        text = item.get("generated_text", "")
        parsed = parse_generated_text(text)
        parsed_items.append({
            "keyword": item.get("keyword"),
            "parsed": parsed,
            "generated_text": text
        })
    os.makedirs(os.path.dirname(REPARSED_OUTPUT_PATH), exist_ok=True)
    with open(REPARSED_OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(parsed_items, f, ensure_ascii=False, indent=2)
    logging.info(f"✅ Parsed results saved to {REPARSED_OUTPUT_PATH}")
    return parsed_items


if __name__ == "__main__":
    try:
        parse_failed_items()
    except Exception:
        exit(1)

