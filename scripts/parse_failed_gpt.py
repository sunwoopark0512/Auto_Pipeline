"""Parse failed GPT outputs and save reparsed results."""

import os
import json
import logging
from dotenv import load_dotenv

from notion_hook_uploader import parse_generated_text

load_dotenv()
FAILED_HOOK_PATH = os.getenv("FAILED_HOOK_PATH", "logs/failed_hooks.json")
REPARSED_OUTPUT_PATH = os.getenv("REPARSED_OUTPUT_PATH", "logs/failed_keywords_reparsed.json")

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

def parse_failed_gpt():
    if not os.path.exists(FAILED_HOOK_PATH):
        logging.info("✅ 실패 파일이 없어 건너뜁니다: %s", FAILED_HOOK_PATH)
        return

    with open(FAILED_HOOK_PATH, 'r', encoding='utf-8') as f:
        items = json.load(f)

    reparsed = []
    for item in items:
        text = item.get("generated_text")
        if not text:
            logging.warning(f"⚠️ generated_text 누락: {item.get('keyword')}")
            continue
        parsed = parse_generated_text(text)
        item["parsed"] = parsed
        reparsed.append(item)

    os.makedirs(os.path.dirname(REPARSED_OUTPUT_PATH), exist_ok=True)
    with open(REPARSED_OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(reparsed, f, ensure_ascii=False, indent=2)
    logging.info("✅ 재파싱 결과 저장: %s", REPARSED_OUTPUT_PATH)

if __name__ == "__main__":
    parse_failed_gpt()
