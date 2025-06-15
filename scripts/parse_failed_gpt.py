import os
import json
import logging
import re

FAILED_PATH = os.getenv("FAILED_HOOK_PATH", "logs/failed_hooks.json")
OUTPUT_PATH = os.getenv("REPARSED_OUTPUT_PATH", "logs/failed_keywords_reparsed.json")

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

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

def parse_failed() -> list:
    if not os.path.exists(FAILED_PATH):
        logging.warning(f"❗ 실패 로그 파일이 없습니다: {FAILED_PATH}")
        return []

    with open(FAILED_PATH, "r", encoding="utf-8") as f:
        items = json.load(f)

    results = []
    for item in items:
        text = item.get("generated_text") or ""
        parsed = parse_generated_text(text)
        item["parsed"] = parsed
        results.append(item)

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    logging.info(f"✅ 파싱된 결과 저장: {OUTPUT_PATH}")
    return results

if __name__ == "__main__":
    parse_failed()
