import os
import json
import logging
from dotenv import load_dotenv

load_dotenv()
FAILED_HOOK_PATH = os.getenv("FAILED_HOOK_PATH", "logs/failed_hooks.json")
REPARSED_OUTPUT_PATH = os.getenv("REPARSED_OUTPUT_PATH", "logs/failed_keywords_reparsed.json")

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')


def parse_gpt_output(text: str):
    """Parse raw GPT text into structured fields."""
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return {
        "hook_lines": lines[:2],
        "blog_paragraphs": lines[2:5],
        "video_titles": lines[5:],
    }


def reparse_failed_items():
    if not os.path.exists(FAILED_HOOK_PATH):
        logging.error(f"❌ 실패 파일이 존재하지 않습니다: {FAILED_HOOK_PATH}")
        return

    try:
        with open(FAILED_HOOK_PATH, 'r', encoding='utf-8') as f:
            failed_items = json.load(f)
    except Exception as e:
        logging.error(f"❌ 실패 파일 읽기 오류: {e}")
        return

    reparsed = []
    for item in failed_items:
        keyword = item.get("keyword")
        text = item.get("generated_text")
        if not keyword or not text:
            logging.warning("⛔ keyword 또는 generated_text 누락 항목 건너뜀")
            continue
        try:
            parsed = parse_gpt_output(text)
            item.update(parsed)
            reparsed.append(item)
            logging.info(f"✅ 파싱 성공: {keyword}")
        except Exception as e:
            logging.error(f"❌ 파싱 실패: {keyword} - {e}")
            item["parse_error"] = str(e)
            reparsed.append(item)

    os.makedirs(os.path.dirname(REPARSED_OUTPUT_PATH), exist_ok=True)
    with open(REPARSED_OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(reparsed, f, ensure_ascii=False, indent=2)
    logging.info(f"📄 파싱 결과 저장 완료: {REPARSED_OUTPUT_PATH}")


if __name__ == "__main__":
    reparse_failed_items()
