"""Parse failed GPT results and save them in a structured form."""

import json
import logging
import os
from typing import List, Dict, Any

from dotenv import load_dotenv
from notion_hook_uploader import parse_generated_text

load_dotenv()
FAILED_PATH = os.getenv("FAILED_HOOK_PATH", "logs/failed_hooks.json")
OUTPUT_PATH = os.getenv("REPARSED_OUTPUT_PATH", "logs/failed_keywords_reparsed.json")

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s:%(message)s")


def parse_failed_items() -> List[Dict[str, Any]]:
    """Parse GPT outputs from ``FAILED_PATH`` and write results to
    ``OUTPUT_PATH``.
    """
    if not os.path.exists(FAILED_PATH):
        logging.info("❗ 실패 파일이 존재하지 않습니다: %s", FAILED_PATH)
        return []

    with open(FAILED_PATH, "r", encoding="utf-8") as file:
        data = json.load(file)

    parsed_items = []
    for item in data:
        text = item.get("generated_text", "")
        parsed = parse_generated_text(text)
        parsed_items.append({
            "keyword": item.get("keyword"),
            "generated_text": text,
            "parsed": parsed,
        })

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as file:
        json.dump(parsed_items, file, ensure_ascii=False, indent=2)

    logging.info("✅ 파싱 완료: %s (항목 %d개)", OUTPUT_PATH, len(parsed_items))
    return parsed_items


if __name__ == "__main__":
    parse_failed_items()
