import os
import json
import logging
from dotenv import load_dotenv
from notion_hook_uploader import parse_generated_text

load_dotenv()
FAILED_HOOK_PATH = os.getenv("FAILED_HOOK_PATH", "logs/failed_hooks.json")
OUTPUT_PATH = os.getenv("REPARSED_OUTPUT_PATH", "logs/failed_keywords_reparsed.json")

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

def reparse_failed_hooks():
    if not os.path.exists(FAILED_HOOK_PATH):
        logging.error(f"❌ 실패 파일이 없습니다: {FAILED_HOOK_PATH}")
        return

    with open(FAILED_HOOK_PATH, 'r', encoding='utf-8') as f:
        items = json.load(f)

    parsed_items = []
    for item in items:
        text = item.get("generated_text")
        if text:
            parsed = parse_generated_text(text)
            item["parsed"] = parsed
        else:
            item["retry_error"] = "no_generated_text"
        parsed_items.append(item)

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(parsed_items, f, ensure_ascii=False, indent=2)

    logging.info(f"✅ 재파싱 결과 저장: {OUTPUT_PATH}")

if __name__ == "__main__":
    reparse_failed_hooks()
