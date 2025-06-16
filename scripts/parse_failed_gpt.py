import os
import sys
import json
import logging
from dotenv import load_dotenv

# Allow importing modules from project root
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from notion_hook_uploader import parse_generated_text

load_dotenv()

FAILED_INPUT_PATH = os.getenv("FAILED_HOOK_PATH", "logs/failed_hooks.json")
OUTPUT_PATH = os.getenv("REPARSED_OUTPUT_PATH", "logs/failed_keywords_reparsed.json")

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')


def load_failed_items():
    if not os.path.exists(FAILED_INPUT_PATH):
        logging.error(f"❌ 입력 파일이 존재하지 않습니다: {FAILED_INPUT_PATH}")
        return []
    with open(FAILED_INPUT_PATH, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except Exception as e:
            logging.error(f"JSON 로딩 실패: {e}")
            return []


def reparse_items(items):
    output = []
    for item in items:
        text = item.get("generated_text")
        if text:
            try:
                item["parsed"] = parse_generated_text(text)
            except Exception as e:
                logging.warning(f"파싱 실패: {item.get('keyword')} - {e}")
        output.append(item)
    return output


def main():
    items = load_failed_items()
    if not items:
        logging.info("재파싱할 항목이 없습니다.")
        return
    reparsed = reparse_items(items)
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(reparsed, f, ensure_ascii=False, indent=2)
    logging.info(f"✅ 재파싱 결과 저장: {OUTPUT_PATH} (총 {len(reparsed)}개)")


if __name__ == "__main__":
    main()
