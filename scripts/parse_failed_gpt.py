import os
import json
import logging
import re
from dotenv import load_dotenv

# ---------------------- 설정 로딩 ----------------------
load_dotenv()
FAILED_HOOK_PATH = os.getenv("FAILED_HOOK_PATH", "logs/failed_hooks.json")
OUTPUT_PATH = os.getenv("REPARSED_OUTPUT_PATH", "logs/failed_keywords_reparsed.json")

# ---------------------- 로깅 설정 ----------------------
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')


# ---------------------- GPT 출력 파싱 ----------------------
def parse_generated_text(text: str) -> dict:
    """Parse GPT generated text into hook lines, blog paragraphs and video titles."""
    hook_lines = re.findall(r"후킹 ?문장[0-9]?[\s:：\-\)]*([^\n]+)", text)
    blog_match = re.search(r"블로그(?:\s*초안)?[\s:：\-\)]*(.*?)\n+\s*(.*?\n+.*?\n+.*?)(?:\n|$)", text, re.DOTALL)
    video_titles = re.findall(r"(?:영상 제목|YouTube 제목)[\s:：\-\)]*[^\n]*\n?-\s*(.+)", text)

    blog_paragraphs = [p.strip() for p in blog_match[1].strip().split('\n')[:3]] if blog_match else ["", "", ""]
    return {
        "hook_lines": hook_lines[:2] if len(hook_lines) >= 2 else ["", ""],
        "blog_paragraphs": blog_paragraphs,
        "video_titles": video_titles[:2] if video_titles else ["", ""]
    }


# ---------------------- 메인 파싱 함수 ----------------------
def parse_failed_gpt() -> None:
    if not os.path.exists(FAILED_HOOK_PATH):
        logging.error(f"❌ 실패 후킹 파일을 찾을 수 없습니다: {FAILED_HOOK_PATH}")
        return

    with open(FAILED_HOOK_PATH, 'r', encoding='utf-8') as f:
        failed_data = json.load(f)

    reparsed = []
    skipped = 0

    for entry in failed_data:
        keyword = entry.get("keyword")
        text = entry.get("generated_text")
        if not keyword or not text:
            logging.warning(f"⛔ 데이터 누락 - keyword: {keyword} text: {bool(text)}")
            skipped += 1
            continue
        parsed = parse_generated_text(text)
        reparsed.append({
            "keyword": keyword,
            "hook_lines": parsed["hook_lines"],
            "blog_paragraphs": parsed["blog_paragraphs"],
            "video_titles": parsed["video_titles"]
        })

    if reparsed:
        os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
        with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
            json.dump(reparsed, f, ensure_ascii=False, indent=2)
        logging.info(f"✅ 파싱 결과 저장: {OUTPUT_PATH}")
    else:
        logging.info("⚠️ 파싱 가능한 항목이 없습니다.")

    logging.info(f"📊 파싱 요약 - 총 {len(failed_data)}개 중 {len(reparsed)}개 성공, {skipped}개 건너뜀")


if __name__ == "__main__":
    parse_failed_gpt()
