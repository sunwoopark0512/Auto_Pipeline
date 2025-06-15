import os
import json
import logging
from dotenv import load_dotenv
from notion_hook_uploader import parse_generated_text

load_dotenv()
FAILED_PATH = os.getenv("FAILED_HOOK_PATH", "logs/failed_keywords.json")
OUTPUT_PATH = os.getenv("REPARSED_OUTPUT_PATH", "logs/failed_keywords_reparsed.json")

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')


def parse_failed_gpt():
    if not os.path.exists(FAILED_PATH):
        logging.warning(f"❗ 실패 항목 파일이 없습니다: {FAILED_PATH}")
        return []

    with open(FAILED_PATH, 'r', encoding='utf-8') as f:
        items = json.load(f)

    reparsed = []
    for item in items:
        text = item.get("generated_text", "")
        item["parsed"] = parse_generated_text(text)
        reparsed.append(item)

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(reparsed, f, ensure_ascii=False, indent=2)

    logging.info(f"📄 재파싱 결과 저장 완료: {OUTPUT_PATH}")
    return reparsed



if __name__ == "__main__":
    parse_failed_gpt()
