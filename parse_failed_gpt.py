import os
import json
import logging
import re
from dotenv import load_dotenv

load_dotenv()

FAILED_INPUT_PATH = os.getenv("FAILED_HOOK_PATH", "data/upload_failed_hooks.json")
OUTPUT_PATH = os.getenv("REPARSED_OUTPUT_PATH", "logs/failed_keywords_reparsed.json")

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

# GPT 결과 파싱 함수 (notion_hook_uploader.py와 동일)
def parse_generated_text(text):
    hook_lines = re.findall(r"후킹 ?문장[0-9]?[\s:：\-\)]*([^\n]+)", text)
    blog_match = re.search(r"블로그(?:\s*초안)?[\s:：\-\)]*(.*?)\n+\s*(.*?\n+.*?\n+.*?)(?:\n|$)", text, re.DOTALL)
    video_titles = re.findall(r"(?:영상 제목|YouTube 제목)[\s:：\-\)]*[^\n]*\n?-\s*(.+)", text)

    blog_paragraphs = [p.strip() for p in blog_match[1].strip().split('\n')[:3]] if blog_match else ["", "", ""]
    return {
        "hook_lines": hook_lines[:2] if len(hook_lines) >= 2 else ["", ""],
        "blog_paragraphs": blog_paragraphs,
        "video_titles": video_titles[:2] if video_titles else ["", ""]
    }

def main():
    if not os.path.exists(FAILED_INPUT_PATH):
        logging.info(f"❌ 실패 항목 파일이 존재하지 않습니다: {FAILED_INPUT_PATH}")
        return

    with open(FAILED_INPUT_PATH, 'r', encoding='utf-8') as f:
        items = json.load(f)

    parsed_items = []
    for item in items:
        text = item.get("generated_text", "")
        parsed = parse_generated_text(text)
        item["parsed"] = parsed
        parsed_items.append(item)

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(parsed_items, f, ensure_ascii=False, indent=2)
    logging.info(f"✅ 파싱 완료: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
