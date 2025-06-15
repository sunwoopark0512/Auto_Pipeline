import asyncio
import json
import logging
import os
from datetime import datetime

from dotenv import load_dotenv
import openai

# ---------------------- 설정 로딩 ----------------------
load_dotenv()
KEYWORD_JSON_PATH = os.getenv("KEYWORD_OUTPUT_PATH", "data/keyword_output_with_cpc.json")
HOOK_OUTPUT_PATH = os.getenv("HOOK_OUTPUT_PATH", "data/generated_hooks.json")
FAILED_HOOK_PATH = os.getenv("FAILED_HOOK_PATH", "logs/failed_hooks.json")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
API_DELAY = float(os.getenv("API_DELAY", "1.0"))
MAX_CONCURRENT_REQUESTS = int(os.getenv("MAX_CONCURRENT_REQUESTS", "5"))

openai.api_key = OPENAI_API_KEY

# ---------------------- 로깅 설정 ----------------------
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

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
async def get_gpt_response(prompt: str, retries: int = 3, delay: float = 2.0) -> str | None:
    """Call OpenAI GPT asynchronously with retry logic."""
    for attempt in range(retries):
        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
            )
            return response.choices[0].message["content"]
        except Exception as exc:  # pragma: no cover - network issues
            logging.warning("GPT 호출 실패 %s/%s: %s", attempt + 1, retries, exc)
            if attempt < retries - 1:
                await asyncio.sleep(delay * (attempt + 1))
    return None

# ---------------------- 메인 실행 함수 ----------------------
async def process_keyword(item: dict, existing: dict, sem: asyncio.Semaphore):
    """Process a single keyword entry using the GPT API."""
    keyword = item.get("keyword")
    if not keyword:
        logging.warning("⛔ 빈 키워드 항목, 건너뜁니다.")
        return "skip", None

    if keyword in existing:
        logging.info("⏭️ 중복 스킵: %s", keyword)
        return "skip", None

    prompt = generate_hook_prompt(
        keyword=keyword,
        topic=keyword.split()[0],
        source=item.get("source"),
        score=item.get("score", 0),
        growth=item.get("growth", 0),
        mentions=item.get("mentions", 0),
    )

    async with sem:
        response = await get_gpt_response(prompt)
        await asyncio.sleep(API_DELAY)

    result: dict = {
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
        logging.info("✅ 생성 완료: %s", keyword)
        return "success", result

    result["generated_text"] = None
    result["error"] = "GPT 응답 실패"
    logging.error("❌ 생성 실패: %s", keyword)
    return "failed", result


async def generate_hooks() -> None:
    if not OPENAI_API_KEY:
        logging.error("❗ OpenAI API 키가 누락되었습니다. .env 파일 확인 필요")
        return

    try:
        with open(KEYWORD_JSON_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            keywords = data.get("filtered_keywords", [])
    except Exception as e:
        logging.error(f"❗ 키워드 파일 읽기 오류: {e}")
        return

    existing = {}
    if os.path.exists(HOOK_OUTPUT_PATH):
        try:
            with open(HOOK_OUTPUT_PATH, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
                for entry in existing_data:
                    existing[entry['keyword']] = entry
        except Exception as e:
            logging.warning(f"기존 결과 로딩 실패: {e}")

    new_output: list[dict] = []
    failed_output: list[dict] = []
    skipped = success = failed = 0

    sem = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)
    tasks = [process_keyword(item, existing, sem) for item in keywords]

    for coro in asyncio.as_completed(tasks):
        status, result = await coro
        if status == "skip":
            skipped += 1
            continue
        if result is None:
            failed += 1
            continue

        if status == "success":
            new_output.append(result)
            success += 1
        else:
            failed_output.append(result)
            failed += 1

    full_output = list(existing.values()) + new_output
    os.makedirs(os.path.dirname(HOOK_OUTPUT_PATH), exist_ok=True)
    with open(HOOK_OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(full_output, f, ensure_ascii=False, indent=2)

    if failed_output:
        os.makedirs(os.path.dirname(FAILED_HOOK_PATH), exist_ok=True)
        with open(FAILED_HOOK_PATH, 'w', encoding='utf-8') as f:
            json.dump(failed_output, f, ensure_ascii=False, indent=2)
        logging.warning(f"⚠️ 실패 후킹 저장 완료: {FAILED_HOOK_PATH}")

    logging.info("📊 생성 작업 요약")
    logging.info(f"총 키워드: {len(keywords)} | 성공: {success} | 중복스킵: {skipped} | 실패: {failed}")
    logging.info(f"🎉 후킹 문장 저장 완료: {HOOK_OUTPUT_PATH}")

if __name__ == "__main__":
    asyncio.run(generate_hooks())
