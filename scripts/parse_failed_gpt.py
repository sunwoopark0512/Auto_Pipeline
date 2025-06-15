import os
import json
import logging
from dotenv import load_dotenv
from notion_hook_uploader import parse_generated_text

load_dotenv()
FAILED_PATH = os.getenv("FAILED_HOOK_PATH", "logs/failed_hooks.json")
OUTPUT_PATH = os.getenv("REPARSED_OUTPUT_PATH", "logs/failed_keywords_reparsed.json")

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')


def load_failed_items():
    if not os.path.exists(FAILED_PATH):
        logging.info(f"❗ 실패 항목 파일이 존재하지 않습니다: {FAILED_PATH}")
        return []
    with open(FAILED_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def parse_items(items):
    parsed = []
    for item in items:
        text = item.get("generated_text")
        if not text:
            logging.warning(f"⛔ generated_text 누락: {item.get('keyword')}")
            continue
        try:
            item["parsed"] = parse_generated_text(text)
            parsed.append(item)
        except Exception as e:
            logging.error(f"❌ 파싱 실패: {item.get('keyword')} - {e}")
    return parsed


def save_parsed(items):
    if not items:
        logging.info("✅ 파싱할 항목이 없습니다.")
        return
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(items, f, ensure_ascii=False, indent=2)
    logging.info(f"📦 파싱 결과 저장: {OUTPUT_PATH} ({len(items)} items)")


def main():
    items = load_failed_items()
    parsed = parse_items(items)
    save_parsed(parsed)


if __name__ == "__main__":
    main()

