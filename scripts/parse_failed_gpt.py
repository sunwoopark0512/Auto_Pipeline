import os
import json
import logging
import re

# notion_hook_uploader 모듈을 직접 임포트하면 로그 파일 경로 문제로 오류가 발생하므로
# 여기에서 필요한 파싱 함수만 간단히 구현한다.
def parse_generated_text(text: str) -> dict:
    hook_lines = re.findall(r"후킹 ?문장[0-9]?[\s:：\-\)]*([^\n]+)", text)
    blog_match = re.search(
        r"블로그(?:\s*초안)?[\s:：\-\)]*(.*?)\n+\s*(.*?\n+.*?\n+.*?)(?:\n|$)",
        text,
        re.DOTALL,
    )
    video_titles = re.findall(r"(?:영상 제목|YouTube 제목)[\s:：\-\)]*[^\n]*\n?-\s*(.+)", text)

    blog_paragraphs = [p.strip() for p in blog_match[1].strip().split('\n')[:3]] if blog_match else ["", "", ""]
    return {
        "hook_lines": hook_lines[:2] if len(hook_lines) >= 2 else ["", ""],
        "blog_paragraphs": blog_paragraphs,
        "video_titles": video_titles[:2] if video_titles else ["", ""],
    }

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

FAILED_PATH = os.getenv("FAILED_UPLOADS_PATH", "logs/failed_uploads.json")
OUTPUT_PATH = os.getenv("REPARSED_OUTPUT_PATH", "logs/failed_keywords_reparsed.json")

def parse_failed_items():
    if not os.path.exists(FAILED_PATH):
        logging.warning(f"❗ 실패 파일이 존재하지 않습니다: {FAILED_PATH}")
        return

    try:
        with open(FAILED_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        logging.error(f"❌ 실패 파일 읽기 오류: {e}")
        return

    reparsed = []
    for item in data:
        text = item.get("generated_text", "")
        parsed = parse_generated_text(text) if text else {"hook_lines": ["", ""], "blog_paragraphs": ["", "", ""], "video_titles": ["", ""]}
        item["parsed"] = parsed
        reparsed.append(item)

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(reparsed, f, ensure_ascii=False, indent=2)
    logging.info(f"✅ 파싱된 결과 저장: {OUTPUT_PATH}")

if __name__ == "__main__":
    parse_failed_items()
