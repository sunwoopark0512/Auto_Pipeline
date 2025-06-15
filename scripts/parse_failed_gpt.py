import os
import json
import logging
import re
from dotenv import load_dotenv

# ---------------------- 설정 로딩 ----------------------
load_dotenv()
FAILED_HOOK_PATH = os.getenv("FAILED_HOOK_PATH", "logs/failed_hooks.json")
REPARSED_OUTPUT_PATH = os.getenv("REPARSED_OUTPUT_PATH", "logs/failed_keywords_reparsed.json")

# ---------------------- 로깅 설정 ----------------------
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

# ---------------------- GPT 결과 파싱 ----------------------
def parse_generated_text(text: str):
    hook_lines = re.findall(r"후킹 ?문장[0-9]?[\s:：\-\)]*([^\n]+)", text)
    blog_match = re.search(r"블로그(?:\s*초안)?[\s:：\-\)]*(.*?)\n+\s*(.*?\n+.*?\n+.*?)(?:\n|$)", text, re.DOTALL)
    video_titles = re.findall(r"(?:영상 제목|YouTube 제목)[\s:：\-\)]*[^\n]*\n?-\s*(.+)", text)

    blog_paragraphs = [p.strip() for p in blog_match[1].strip().split('\n')[:3]] if blog_match else ["", "", ""]
    return {
        "hook_lines": hook_lines[:2] if len(hook_lines) >= 2 else ["", ""],
        "blog_paragraphs": blog_paragraphs,
        "video_titles": video_titles[:2] if video_titles else ["", ""]
    }

# ---------------------- 실패 GPT 재파싱 ----------------------
def parse_failed_gpt():
    if not os.path.exists(FAILED_HOOK_PATH):
        logging.error(f"❌ 실패 파일이 존재하지 않습니다: {FAILED_HOOK_PATH}")
        return

    with open(FAILED_HOOK_PATH, 'r', encoding='utf-8') as f:
        failed_items = json.load(f)

    reparsed = []
    for item in failed_items:
        keyword = item.get('keyword')
        if not keyword:
            logging.warning("⛔ keyword 누락 항목 건너뜁니다.")
            continue
        text = item.get('generated_text') or ''
        parsed = parse_generated_text(text)
        reparsed.append({
            'keyword': keyword,
            'hook_lines': parsed['hook_lines'],
            'blog_paragraphs': parsed['blog_paragraphs'],
            'video_titles': parsed['video_titles']
        })

    os.makedirs(os.path.dirname(REPARSED_OUTPUT_PATH), exist_ok=True)
    with open(REPARSED_OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(reparsed, f, ensure_ascii=False, indent=2)

    logging.info(f"✅ 재파싱 완료: {len(reparsed)}개 항목 저장 -> {REPARSED_OUTPUT_PATH}")

if __name__ == "__main__":
    parse_failed_gpt()
