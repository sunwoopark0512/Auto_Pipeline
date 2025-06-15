import os
import json
import logging
import sys

# allow import from project root
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from notion_hook_uploader import parse_generated_text

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

INPUT_PATH = os.getenv("FAILED_HOOK_PATH", "logs/failed_hooks.json")
OUTPUT_PATH = os.getenv("REPARSED_OUTPUT_PATH", "logs/failed_keywords_reparsed.json")


def parse_failed_items():
    if not os.path.exists(INPUT_PATH):
        logging.warning(f"❗ 입력 파일이 존재하지 않습니다: {INPUT_PATH}")
        return

    with open(INPUT_PATH, 'r', encoding='utf-8') as f:
        failed = json.load(f)

    reparsed = []
    for item in failed:
        keyword = item.get("keyword")
        entry = {"keyword": keyword}
        text = item.get("generated_text") or ""
        if text:
            try:
                entry["parsed"] = parse_generated_text(text)
            except Exception as e:
                entry["parse_error"] = str(e)
        else:
            entry["parse_error"] = item.get("error", "no generated text")
        reparsed.append(entry)

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(reparsed, f, ensure_ascii=False, indent=2)

    logging.info(f"📑 변환된 실패 항목 {len(reparsed)}개 저장: {OUTPUT_PATH}")


if __name__ == "__main__":
    parse_failed_items()
