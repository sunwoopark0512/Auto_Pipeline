import os
import json
import logging
import re
from dotenv import load_dotenv

# ---------------------- 설정 로딩 ----------------------
load_dotenv()
FAILED_HOOK_PATH = os.getenv("FAILED_HOOK_PATH", "logs/failed_hooks.json")
REPARSED_OUTPUT_PATH = os.getenv("REPARSED_OUTPUT_PATH", "logs/failed_keywords_reparsed.json")

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

# ---------------------- GPT 응답 파싱 ----------------------
def parse_gpt_text(text: str):
    """주어진 GPT 응답 문자열을 후킹문, 블로그 문단, 영상 제목으로 분리합니다."""
    if not text:
        return {
            "hook_lines": ["", ""],
            "blog_paragraphs": ["", "", ""],
            "video_titles": ["", ""]
        }

    cleaned = []
    for line in text.splitlines():
        line = line.strip()
        # 숫자/기호로 시작하는 패턴 제거
        line = re.sub(r"^[\-*\d.()\s]+", "", line)
        if line:
            cleaned.append(line)

    while len(cleaned) < 7:
        cleaned.append("")

    return {
        "hook_lines": cleaned[0:2],
        "blog_paragraphs": cleaned[2:5],
        "video_titles": cleaned[5:7]
    }

# ---------------------- 실패 데이터 로딩 ----------------------
def load_failed_hooks():
    if not os.path.exists(FAILED_HOOK_PATH):
        logging.error(f"❌ 실패 데이터 파일이 없습니다: {FAILED_HOOK_PATH}")
        return []
    with open(FAILED_HOOK_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

# ---------------------- 재파싱 수행 ----------------------
def reparse_failed_hooks():
    hooks = load_failed_hooks()
    if not hooks:
        logging.info("✅ 재파싱할 항목이 없습니다.")
        return

    parsed_items = []
    for item in hooks:
        keyword = item.get("keyword")
        if not keyword:
            logging.warning("⛔ keyword 누락 항목 건너뜁니다.")
            continue
        text = item.get("generated_text") or item.get("error", "")
        parsed = parse_gpt_text(text)
        parsed_item = {
            "keyword": keyword,
            "parsed": parsed,
            "hook_prompt": item.get("hook_prompt"),
            "timestamp": item.get("timestamp"),
        }
        # 상위 호환을 위해 기본 필드도 제공
        parsed_item.update(parsed)
        if item.get("error"):
            parsed_item["original_error"] = item.get("error")
        parsed_items.append(parsed_item)

    os.makedirs(os.path.dirname(REPARSED_OUTPUT_PATH), exist_ok=True)
    with open(REPARSED_OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(parsed_items, f, ensure_ascii=False, indent=2)

    logging.info(f"📑 재파싱 결과 저장 완료: {REPARSED_OUTPUT_PATH}")
    logging.info(f"총 항목: {len(parsed_items)}")

if __name__ == "__main__":
    reparse_failed_hooks()
