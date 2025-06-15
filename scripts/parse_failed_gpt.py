import os
import json
import logging
import re
from dotenv import load_dotenv  # type: ignore

# ---------------------- 설정 로딩 ----------------------
load_dotenv()
FAILED_HOOK_PATH = os.getenv("FAILED_HOOK_PATH", "logs/failed_hooks.json")
REPARSED_OUTPUT_PATH = os.getenv("REPARSED_OUTPUT_PATH", "logs/failed_keywords_reparsed.json")

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

# ---------------------- GPT 결과 파싱 함수 ----------------------
def parse_generated_text(text: str) -> dict:
    """Parse GPT output text into components."""
    hook_lines = re.findall(r"후킹 ?문장[0-9]?[\s:：\-\)]*([^\n]+)", text)
    blog_match = re.search(
        r"블로그(?:\s*초안)?[\s:：\-\)]*(.*?)\n+\s*(.*?\n+.*?\n+.*?)(?:\n|$)",
        text,
        re.DOTALL,
    )
    video_titles = re.findall(r"(?:영상 제목|YouTube 제목)[\s:：\-\)]*[^\n]*\n?-\s*(.+)", text)

    blog_paragraphs = [p.strip() for p in blog_match[1].strip().split("\n")[:3]] if blog_match else ["", "", ""]
    return {
        "hook_lines": hook_lines[:2] if len(hook_lines) >= 2 else ["", ""],
        "blog_paragraphs": blog_paragraphs,
        "video_titles": video_titles[:2] if video_titles else ["", ""],
    }

# ---------------------- 실패 기록 로딩 ----------------------
def load_failed_items(path: str) -> list:
    if not os.path.exists(path):
        logging.error(f"❌ 실패 항목 파일이 없습니다: {path}")
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# ---------------------- 메인 파싱 로직 ----------------------
def reparse_failed_outputs() -> None:
    failed_items = load_failed_items(FAILED_HOOK_PATH)
    if not failed_items:
        logging.info("✅ 파싱할 실패 항목이 없습니다.")
        return

    reparsed = []
    for item in failed_items:
        keyword = item.get("keyword", "")
        text = item.get("generated_text", "") or ""
        parsed = parse_generated_text(text)
        reparsed.append({
            "keyword": keyword,
            **parsed,
        })
    os.makedirs(os.path.dirname(REPARSED_OUTPUT_PATH), exist_ok=True)
    with open(REPARSED_OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(reparsed, f, ensure_ascii=False, indent=2)
    logging.info(f"📑 재파싱 결과 저장: {REPARSED_OUTPUT_PATH}")
    logging.info(f"총 항목: {len(reparsed)}")

if __name__ == "__main__":
    reparse_failed_outputs()
