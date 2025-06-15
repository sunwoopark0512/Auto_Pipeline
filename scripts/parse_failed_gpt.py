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
        logging.error(f"❌ 실패 파일이 없습니다: {FAILED_PATH}")
        return []
    with open(FAILED_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def parse_items(items):
    parsed = []
    for item in items:
        keyword = item.get("keyword")
        text = item.get("generated_text", "")
        result = {
            "keyword": keyword,
            "generated_text": text,
            "parsed": parse_generated_text(text) if text else {
                "hook_lines": ["", ""],
                "blog_paragraphs": ["", "", ""],
                "video_titles": ["", ""]
            }
        }
        parsed.append(result)
    return parsed

def main():
    items = load_failed_items()
    if not items:
        logging.info("✅ 파싱할 항목이 없습니다.")
        return

    parsed = parse_items(items)
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(parsed, f, ensure_ascii=False, indent=2)
    logging.info(f"✅ 재파싱 결과 저장 완료: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
