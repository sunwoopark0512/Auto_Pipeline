import os
import json
import logging
from datetime import datetime
from dotenv import load_dotenv
import asyncio

from scripts.ai_async import batch_generate

# ---------------------- 설정 로딩 ----------------------
load_dotenv()
KEYWORD_JSON_PATH = os.getenv("KEYWORD_OUTPUT_PATH", "data/keyword_output_with_cpc.json")
HOOK_OUTPUT_PATH = os.getenv("HOOK_OUTPUT_PATH", "data/generated_hooks.json")
FAILED_HOOK_PATH = os.getenv("FAILED_HOOK_PATH", "logs/failed_hooks.json")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CONCURRENCY = int(os.getenv("CONCURRENCY", "5"))

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

# ---------------------- GPT 비동기 호출 ----------------------


# ---------------------- 메인 실행 함수 ----------------------
async def _generate_hooks():
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
    skipped, success, failed = 0, 0, 0

    prompts = []
    items = []
    for item in keywords:
        keyword = item.get('keyword')
        if not keyword:
            logging.warning("⛔ 빈 키워드 항목, 건너뜁니다.")
            continue

        if keyword in existing:
            logging.info(f"⏭️ 중복 스킵: {keyword}")
            skipped += 1
            continue

        prompt = generate_hook_prompt(
            keyword=keyword,
            topic=keyword.split()[0],
            source=item.get('source'),
            score=item.get('score', 0),
            growth=item.get('growth', 0),
            mentions=item.get('mentions', 0)
        )
        prompts.append(prompt)
        items.append(keyword)

    responses = await batch_generate(prompts, concurrency=CONCURRENCY)

    for keyword, prompt, response in zip(items, prompts, responses):
        result = {
            "keyword": keyword,
            "hook_prompt": prompt,
            "timestamp": datetime.utcnow().isoformat() + 'Z'
        }

        if response:
            lines = response.split('\n')
            result.update({
                "hook_lines": lines[0:2],
                "blog_paragraphs": lines[2:5],
                "video_titles": lines[5:],
                "generated_text": response
            })
            new_output.append(result)
            logging.info(f"✅ 생성 완료: {keyword}")
            success += 1
        else:
            result["generated_text"] = None
            result["error"] = "GPT 응답 실패"
            failed_output.append(result)
            logging.error(f"❌ 생성 실패: {keyword}")
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


def generate_hooks() -> None:
    asyncio.run(_generate_hooks())

if __name__ == "__main__":
    generate_hooks()
