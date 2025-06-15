import os
import json
import re
import logging
from dotenv import load_dotenv

# ---------------------- 설정 로딩 ----------------------
load_dotenv()
FAILED_HOOK_PATH = os.getenv("FAILED_HOOK_PATH", "logs/failed_hooks.json")
OUTPUT_PATH = os.getenv("REPARSED_OUTPUT_PATH", "logs/failed_keywords_reparsed.json")

# ---------------------- 로깅 설정 ----------------------
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

# ---------------------- GPT 결과 파싱 함수 ----------------------
def parse_generated_text(text: str) -> dict:
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

# ---------------------- 메인 실행 함수 ----------------------
def parse_failed_hooks() -> None:
    if not os.path.exists(FAILED_HOOK_PATH):
        logging.error(f"❌ 실패 후킹 파일이 존재하지 않습니다: {FAILED_HOOK_PATH}")
        return

    with open(FAILED_HOOK_PATH, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except Exception as e:  # pragma: no cover - simple logging
            logging.error(f"❌ JSON 로딩 실패: {e}")
            return

    parsed_results = []
    for item in data:
        keyword = item.get("keyword", "")
        parsed = parse_generated_text(item.get("generated_text", ""))
        parsed_results.append(
            {
                "keyword": keyword,
                "hook_lines": parsed["hook_lines"],
                "blog_paragraphs": parsed["blog_paragraphs"],
                "video_titles": parsed["video_titles"],
            }
        )

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(parsed_results, f, ensure_ascii=False, indent=2)

    logging.info(f"✅ 재파싱 완료: {OUTPUT_PATH} (총 {len(parsed_results)}개)")

if __name__ == "__main__":
    parse_failed_hooks()
