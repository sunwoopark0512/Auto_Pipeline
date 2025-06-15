"""GPT 기반 콘텐츠 리라이팅 모듈."""

import os
import json
import time
import logging
from datetime import datetime
from dotenv import load_dotenv
import openai

# ---------------------- 설정 로딩 ----------------------
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
INPUT_PATH = os.getenv("REWRITE_INPUT_PATH", "data/original_contents.json")
OUTPUT_PATH = os.getenv("REWRITE_OUTPUT_PATH", "data/rewritten_contents.json")
API_DELAY = float(os.getenv("REWRITE_API_DELAY", "1.0"))

openai.api_key = OPENAI_API_KEY

# ---------------------- 로깅 설정 ----------------------
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

# ---------------------- GPT 프롬프트 생성 ----------------------
def generate_rewrite_prompt(text: str) -> str:
    """리라이팅에 사용할 GPT 프롬프트를 생성한다."""
    base = f"""
    다음 콘텐츠를 더 매력적이고 이해하기 쉽게 리라이팅해줘.

{text}

결과는 같은 언어로 간결하게 작성해줘.
    """
    return base.strip()

# ---------------------- GPT 호출 (재시도 포함) ----------------------
def get_rewritten_text(text: str, retries: int = 3) -> str | None:
    """GPT를 호출해 콘텐츠를 리라이팅한다."""
    prompt = generate_rewrite_prompt(text)
    for attempt in range(retries):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
            )
            return response.choices[0].message["content"]
        except Exception as e:
            logging.warning(f"GPT 호출 실패 {attempt + 1}/{retries}: {e}")
            time.sleep(2)
    return None

# ---------------------- 메인 실행 함수 ----------------------
def rewrite_all() -> None:
    """입력 파일의 모든 콘텐츠를 리라이팅하여 저장한다."""
    if not OPENAI_API_KEY:
        logging.error("❗ OpenAI API 키가 누락되었습니다. .env 파일을 확인하세요.")
        return

    try:
        with open(INPUT_PATH, 'r', encoding='utf-8') as f:
            items = json.load(f)
    except Exception as e:
        logging.error(f"❗ 입력 파일 로딩 오류: {e}")
        return

    results: list[dict] = []
    for item in items:
        content = item.get('content')
        if not content:
            logging.warning("⛔ 빈 콘텐츠 항목, 건너뜁니다.")
            continue

        rewritten = get_rewritten_text(content)
        results.append({
            "id": item.get("id"),
            "original_content": content,
            "rewritten_content": rewritten or "",
            "timestamp": datetime.utcnow().isoformat() + 'Z'
        })

        if rewritten:
            logging.info(f"✅ 리라이팅 완료: {item.get('id')}")
        else:
            logging.error(f"❌ 리라이팅 실패: {item.get('id')}")

        time.sleep(API_DELAY)

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    logging.info(f"🎉 리라이팅 결과 저장 완료: {OUTPUT_PATH}")

if __name__ == "__main__":
    rewrite_all()
