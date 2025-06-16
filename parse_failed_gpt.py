import os
import json
import logging
from notion_hook_uploader import parse_generated_text

FAILED_INPUT_PATH = os.getenv("FAILED_HOOK_PATH", "logs/failed_hooks.json")
OUTPUT_PATH = os.getenv("REPARSED_OUTPUT_PATH", "logs/failed_keywords_reparsed.json")

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

def main():
    if not os.path.exists(FAILED_INPUT_PATH):
        logging.info(f"❗ 입력 파일이 존재하지 않습니다: {FAILED_INPUT_PATH}")
        return

    with open(FAILED_INPUT_PATH, 'r', encoding='utf-8') as f:
        items = json.load(f)

    parsed_items = []
    for item in items:
        keyword = item.get("keyword")
        if not keyword:
            continue
        parsed_items.append({
            "keyword": keyword,
            "parsed": parse_generated_text(item.get("generated_text", ""))
        })

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(parsed_items, f, ensure_ascii=False, indent=2)
    logging.info(f"✅ 파싱 완료: {len(parsed_items)}건 저장 -> {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
