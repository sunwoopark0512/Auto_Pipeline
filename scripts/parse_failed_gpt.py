import os
import json
import logging
import re
from dotenv import load_dotenv

load_dotenv()

FAILED_HOOK_PATH = os.getenv("FAILED_HOOK_PATH", "logs/failed_hooks.json")
OUTPUT_PATH = os.getenv("REPARSED_OUTPUT_PATH", "logs/failed_keywords_reparsed.json")

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')


def parse_generated_text(text: str) -> dict:
    """Parse GPT free-form text into structured fields."""
    hook_lines = re.findall(r"후킹 ?문장[0-9]?[\s:：\-\)]*([^\n]+)", text)
    blog_match = re.search(
        r"블로그(?:\s*초안)?[\s:：\-\)]*(.*?)\n+\s*(.*?\n+.*?\n+.*?)(?:\n|$)",
        text,
        re.DOTALL,
    )
    video_titles = re.findall(r"(?:영상 제목|YouTube 제목)[\s:：\-\)]*[^\n]*\n?-\s*(.+)", text)

    blog_paragraphs = (
        [p.strip() for p in blog_match[1].strip().split("\n")[:3]]
        if blog_match
        else ["", "", ""]
    )
    return {
        "hook_lines": hook_lines[:2] if len(hook_lines) >= 2 else ["", ""],
        "blog_paragraphs": blog_paragraphs,
        "video_titles": video_titles[:2] if video_titles else ["", ""],
    }


def reparse_failed_hooks() -> None:
    if not os.path.exists(FAILED_HOOK_PATH):
        logging.error(f"❌ 실패 후킹 파일이 없습니다: {FAILED_HOOK_PATH}")
        return

    try:
        with open(FAILED_HOOK_PATH, "r", encoding="utf-8") as f:
            failed_items = json.load(f)
    except Exception as e:  # pylint: disable=broad-except
        logging.error(f"❗ 실패 파일 읽기 오류: {e}")
        return

    results = []
    for item in failed_items:
        keyword = item.get("keyword")
        if not keyword:
            logging.warning("⛔ keyword 누락 항목 건너뜁니다.")
            continue
        text = item.get("generated_text", "")
        parsed = parse_generated_text(text)
        results.append({
            "keyword": keyword,
            "hook_lines": parsed["hook_lines"],
            "blog_paragraphs": parsed["blog_paragraphs"],
            "video_titles": parsed["video_titles"],
        })

    try:
        os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
        with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        logging.info(f"✅ 재파싱 결과 저장 완료: {OUTPUT_PATH}")
    except Exception as e:  # pylint: disable=broad-except
        logging.error(f"❌ 결과 저장 실패: {e}")


if __name__ == "__main__":
    reparse_failed_hooks()
