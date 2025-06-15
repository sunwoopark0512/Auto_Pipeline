import os
import json
import logging
import re
from dotenv import load_dotenv

# ---------------------- 환경 변수 로딩 ----------------------
load_dotenv()
FAILED_HOOK_PATH = os.getenv("FAILED_HOOK_PATH", "logs/failed_hooks.json")
REPARSED_OUTPUT_PATH = os.getenv("REPARSED_OUTPUT_PATH", "logs/failed_keywords_reparsed.json")

# ---------------------- 로깅 설정 ----------------------
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

# ---------------------- GPT 결과 파싱 ----------------------
def parse_generated_text(text: str):
    """Extract hook lines, blog paragraphs and video titles from GPT text."""
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


# ---------------------- 메인 로직 ----------------------
def parse_failed_gpt():
    """Read failed GPT hooks, parse text and save structured output."""
    if not os.path.exists(FAILED_HOOK_PATH):
        logging.error(f"❌ 실패 파일이 존재하지 않습니다: {FAILED_HOOK_PATH}")
        return

    with open(FAILED_HOOK_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    parsed_results = []
    success, failed = 0, 0
    for item in data:
        keyword = item.get("keyword", "")
        raw_text = item.get("generated_text", "")
        if not raw_text:
            logging.warning(f"⛔ generated_text 없음, 건너뜀: {keyword}")
            failed += 1
            continue
        parsed = parse_generated_text(raw_text)
        parsed_results.append({
            "keyword": keyword,
            "hook_lines": parsed["hook_lines"],
            "blog_paragraphs": parsed["blog_paragraphs"],
            "video_titles": parsed["video_titles"],
        })
        success += 1

    os.makedirs(os.path.dirname(REPARSED_OUTPUT_PATH), exist_ok=True)
    with open(REPARSED_OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(parsed_results, f, ensure_ascii=False, indent=2)

    logging.info("📑 실패 GPT 결과 재파싱 완료")
    logging.info(
        f"총 항목: {len(data)} | 파싱 성공: {success} | 파싱 실패: {failed} | 저장 경로: {REPARSED_OUTPUT_PATH}"
    )


if __name__ == "__main__":
    parse_failed_gpt()
