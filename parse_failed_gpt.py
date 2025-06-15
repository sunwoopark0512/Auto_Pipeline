import json
import logging
import os
from typing import List, Dict, Optional

from notion_hook_uploader import parse_generated_text

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')


def parse_failed(input_path: Optional[str] = None, output_path: Optional[str] = None) -> None:
    """Parse failed GPT results and save them for retry."""
    input_path = input_path or os.getenv("FAILED_HOOK_PATH", "logs/failed_hooks.json")
    output_path = output_path or os.getenv("REPARSED_OUTPUT_PATH", "logs/failed_keywords_reparsed.json")
    assert input_path is not None
    assert output_path is not None

    if not os.path.exists(input_path):
        logging.info(f"❗ 실패 로그 파일이 존재하지 않습니다: {input_path}")
        return

    with open(input_path, "r", encoding="utf-8") as f:
        items: List[Dict] = json.load(f)

    reparsed: List[Dict] = []
    for item in items:
        text = item.get("generated_text")
        keyword = item.get("keyword")
        if text:
            item["parsed"] = parse_generated_text(text)
        else:
            logging.warning(f"✅ 재시도 필요: '{keyword}' 는 generated_text가 없습니다")
        reparsed.append(item)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(reparsed, f, ensure_ascii=False, indent=2)
    logging.info(f"📄 재파싱 결과 저장: {output_path}")


if __name__ == "__main__":
    parse_failed()
