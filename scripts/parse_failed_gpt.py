import os
import json
import logging
from dotenv import load_dotenv

load_dotenv()
FAILED_INPUT_PATH = os.getenv("FAILED_HOOK_PATH", "logs/failed_hooks.json")
OUTPUT_PATH = os.getenv("REPARSED_OUTPUT_PATH", "logs/failed_keywords_reparsed.json")

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

def parse_failed_items():
    if not os.path.exists(FAILED_INPUT_PATH):
        logging.warning(f"\u2757\ufe0f 실패 파일이 존재하지 않습니다: {FAILED_INPUT_PATH}")
        return
    with open(FAILED_INPUT_PATH, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except Exception as e:
            logging.error(f"JSON 로딩 실패: {e}")
            return

    parsed = []
    for item in data:
        parsed.append({
            "keyword": item.get("keyword"),
            "hook_prompt": item.get("hook_prompt"),
            "error": item.get("error"),
            "timestamp": item.get("timestamp"),
        })

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(parsed, f, ensure_ascii=False, indent=2)
    logging.info(f"\uD83D\uDD0D 실패 항목 {len(parsed)}개 파싱 완료: {OUTPUT_PATH}")

if __name__ == "__main__":
    parse_failed_items()
