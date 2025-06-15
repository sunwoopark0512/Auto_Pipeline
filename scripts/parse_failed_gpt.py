import os
import json
import logging
import re
from dotenv import load_dotenv

load_dotenv()

FAILED_HOOK_PATH = os.getenv("FAILED_HOOK_PATH", "logs/failed_hooks.json")
REPARSED_OUTPUT_PATH = os.getenv("REPARSED_OUTPUT_PATH", "logs/failed_keywords_reparsed.json")

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')


def parse_generated_text(text: str) -> dict:
    """Extract structured fields from GPT output text.

    The function first attempts a regex based extraction. If that fails,
    it falls back to a simple line split approach similar to the one used
    during generation.
    """

    hook_lines: list[str] = []
    blog_paragraphs: list[str] = []
    video_titles: list[str] = []
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    section = "hook"
    for line in lines:
        if line.startswith("블로그"):
            section = "blog"
            continue
        if "영상" in line or "YouTube" in line:
            section = "video"
            continue

        if section == "hook" and len(hook_lines) < 2:
            cleaned = re.sub(r"후킹 ?문장[0-9]?[\s:：\-\)]*", "", line)
            hook_lines.append(cleaned)
        elif section == "blog" and len(blog_paragraphs) < 3:
            blog_paragraphs.append(line)
        elif section == "video" and len(video_titles) < 2:
            video_titles.append(line)

    return {
        "hook_lines": (hook_lines + ["", ""])[:2],
        "blog_paragraphs": (blog_paragraphs + ["", "", ""])[:3],
        "video_titles": (video_titles + ["", ""])[:2],
    }


def reparse_failed_gpt() -> None:
    if not os.path.exists(FAILED_HOOK_PATH):
        logging.error(f"❌ 실패 파일이 존재하지 않습니다: {FAILED_HOOK_PATH}")
        return

    with open(FAILED_HOOK_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    logging.info(f"📂 불러온 실패 항목: {len(data)}개")

    reparsed = []
    for item in data:
        keyword = item.get("keyword")
        if not keyword:
            logging.warning("⛔ keyword 누락 항목 건너뜀")
            continue
        text = item.get("generated_text", "") or ""
        parsed = parse_generated_text(text)
        reparsed.append({
            "keyword": keyword,
            "hook_lines": parsed["hook_lines"],
            "blog_paragraphs": parsed["blog_paragraphs"],
            "video_titles": parsed["video_titles"],
        })
        logging.debug(f"✅ 파싱 완료: {keyword}")

    os.makedirs(os.path.dirname(REPARSED_OUTPUT_PATH), exist_ok=True)
    with open(REPARSED_OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(reparsed, f, ensure_ascii=False, indent=2)

    logging.info(f"✅ 재파싱 결과 저장: {REPARSED_OUTPUT_PATH}")
    logging.info(f"총 파싱 성공: {len(reparsed)}")


if __name__ == "__main__":
    reparse_failed_gpt()
