"""SEO optimized content generator."""

import os
import time
import json
import logging
from datetime import datetime
from dotenv import load_dotenv
import openai

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
HOOK_JSON_PATH = os.getenv("HOOK_OUTPUT_PATH", "data/generated_hooks.json")
CONTENT_OUTPUT_PATH = os.getenv("CONTENT_OUTPUT_PATH", "data/seo_contents.json")
API_DELAY = float(os.getenv("API_DELAY", "1.0"))

openai.api_key = OPENAI_API_KEY

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')


def generate_content(keyword: str, paragraphs: int = 3) -> str:
    """Return SEO optimized blog content for a keyword."""
    prompt = (
        f"주제: {keyword}\n"
        f"위 주제에 대해 SEO에 최적화된 {paragraphs}문단 블로그 글을 생성해줘.\n"
        "문체는 친근하면서도 전문가의 느낌을 주도록 하고, 각 문단은 200자 이내로 작성해줘."
    )
    response = openai.ChatCompletion.create(  # pylint: disable=no-member
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    return response.choices[0].message["content"]


def generate_all_contents():
    """Generate content for all keywords in HOOK_JSON_PATH."""
    if not OPENAI_API_KEY:
        logging.error("OPENAI_API_KEY not set")
        return

    try:
        with open(HOOK_JSON_PATH, "r", encoding="utf-8") as file:
            hooks = json.load(file)
    except Exception as exc:  # pylint: disable=broad-except
        logging.error("Failed to load hook file: %s", exc)
        return

    outputs = []
    for item in hooks:
        keyword = item.get("keyword")
        if not keyword:
            logging.warning("Keyword missing, skipped")
            continue
        try:
            content = generate_content(keyword)
            outputs.append(
                {
                    "keyword": keyword,
                    "content": content,
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                }
            )
            logging.info("Content generated: %s", keyword)
        except Exception as exc:  # pylint: disable=broad-except
            logging.error("Content generation failed for %s: %s", keyword, exc)
        finally:
            time.sleep(API_DELAY)

    os.makedirs(os.path.dirname(CONTENT_OUTPUT_PATH), exist_ok=True)
    with open(CONTENT_OUTPUT_PATH, "w", encoding="utf-8") as file:
        json.dump(outputs, file, ensure_ascii=False, indent=2)
    logging.info("Saved all contents to %s", CONTENT_OUTPUT_PATH)


if __name__ == "__main__":
    generate_all_contents()
