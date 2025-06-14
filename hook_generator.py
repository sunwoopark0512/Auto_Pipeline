"""Generate marketing hooks using GPT and collected keywords."""

import json
import logging
import os
import time
from datetime import datetime

import openai
from dotenv import load_dotenv

from scripts.tracing import span

# ---------------------- 설정 로딩 ----------------------
load_dotenv()
KEYWORD_JSON_PATH = os.getenv("KEYWORD_OUTPUT_PATH", "data/keyword_output_with_cpc.json")
HOOK_OUTPUT_PATH = os.getenv("HOOK_OUTPUT_PATH", "data/generated_hooks.json")
FAILED_HOOK_PATH = os.getenv("FAILED_HOOK_PATH", "logs/failed_hooks.json")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
API_DELAY = float(os.getenv("API_DELAY", "1.0"))

openai.api_key = OPENAI_API_KEY

# ---------------------- 로깅 설정 ----------------------
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s:%(message)s")


# ---------------------- GPT 프롬프트 생성 함수 ----------------------
def generate_hook_prompt(keyword, topic, source, score, growth, mentions):
    base = f"""
    주제: {keyword}
    출처: {source}
    트렌드 점수: {score}, 성장률: {growth}, 트윗 수: {mentions}
    이 정보를 기반으로:
    - 숏폼 영상의 후킹 문장 2개
    - 블로그 포스트의 3문단 초안
    - YouTube 영상 제목 예시 2개
    를 마케팅적으로 끌리는 문장으로 생성해줘. 말투는 친근하면서도 전문가처럼.
    """
    return base.strip()


# ---------------------- GPT 호출 함수 (재시도 포함) ----------------------
def get_gpt_response(prompt, retries=3):
    for attempt in range(retries):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
            )
            return response.choices[0].message["content"]
        except Exception as e:
            logging.warning("GPT 호출 실패 %d/%d: %s", attempt + 1, retries, e)
            time.sleep(2)
    return None


# ---------------------- 메인 실행 함수 ----------------------
def generate_hooks():
    if not OPENAI_API_KEY:
        logging.error("❗ OpenAI API 키가 누락되었습니다. .env 파일 확인 필요")
        return

    try:
        with open(KEYWORD_JSON_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            keywords = data.get("filtered_keywords", [])
    except Exception as e:
        logging.error("\u2757 키워드 파일 읽기 오류: %s", e)
        return

    existing = {}
    if os.path.exists(HOOK_OUTPUT_PATH):
        try:
            with open(HOOK_OUTPUT_PATH, "r", encoding="utf-8") as f:
                existing_data = json.load(f)
                for entry in existing_data:
                    existing[entry["keyword"]] = entry
        except Exception as e:
            logging.warning("기존 결과 로딩 실패: %s", e)

    new_output = []
    failed_output = []
    skipped, success, failed = 0, 0, 0

    for item in keywords:
        keyword = item.get("keyword")
        if not keyword:
            logging.warning("⛔ 빈 키워드 항목, 건너뜁니다.")
            continue

        if keyword in existing:
            logging.info("\u23ed\ufe0f 중복 스킵: %s", keyword)
            skipped += 1
            continue

        prompt = generate_hook_prompt(
            keyword=keyword,
            topic=keyword.split()[0],
            source=item.get("source"),
            score=item.get("score", 0),
            growth=item.get("growth", 0),
            mentions=item.get("mentions", 0),
        )
        with span("gpt.api", keyword=keyword):
            response = get_gpt_response(prompt)

        result = {
            "keyword": keyword,
            "hook_prompt": prompt,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }

        if response:
            lines = response.split("\n")
            result.update(
                {
                    "hook_lines": lines[0:2],
                    "blog_paragraphs": lines[2:5],
                    "video_titles": lines[5:],
                    "generated_text": response,
                }
            )
            new_output.append(result)
            logging.info("\u2705 생성 완료: %s", keyword)
            success += 1
        else:
            result["generated_text"] = None
            result["error"] = "GPT 응답 실패"
            failed_output.append(result)
            logging.error("\u274c 생성 실패: %s", keyword)
            failed += 1

        time.sleep(API_DELAY)

    full_output = list(existing.values()) + new_output
    os.makedirs(os.path.dirname(HOOK_OUTPUT_PATH), exist_ok=True)
    with open(HOOK_OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(full_output, f, ensure_ascii=False, indent=2)

    if failed_output:
        os.makedirs(os.path.dirname(FAILED_HOOK_PATH), exist_ok=True)
        with open(FAILED_HOOK_PATH, "w", encoding="utf-8") as f:
            json.dump(failed_output, f, ensure_ascii=False, indent=2)
        logging.warning("\u26a0\ufe0f 실패 후킹 저장 완료: %s", FAILED_HOOK_PATH)

    logging.info("📊 생성 작업 요약")
    logging.info(
        "총 키워드: %d | 성공: %d | 중복스킵: %d | 실패: %d",
        len(keywords),
        success,
        skipped,
        failed,
    )
    logging.info("\U0001f389 후킹 문장 저장 완료: %s", HOOK_OUTPUT_PATH)


if __name__ == "__main__":
    generate_hooks()
