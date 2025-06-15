import os
import json
import logging
from datetime import datetime
from dotenv import load_dotenv
import openai

# ---------------------- 환경 로딩 ----------------------
load_dotenv()
TOPIC_PATH = os.getenv("TOPIC_CHANNELS_PATH", "config/topic_channels.json")
OUTPUT_PATH = os.getenv("KEYWORD_GEN_OUTPUT_PATH", "data/generated_keywords.json")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

# ---------------------- 키워드 생성 ----------------------
def generate_keywords(topic: str):
    prompt = (
        f"'{topic}'와 관련해 지금 한국에서 관심을 끌 만한 키워드 5개를 알려줘. "
        "각 키워드는 짧은 단어 형태로 제공해줘."
    )
    response = openai.ChatCompletion.create(  # type: ignore[attr-defined]
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    lines = response.choices[0].message["content"].splitlines()
    return [line.lstrip("-•– ") for line in lines if line.strip()]

# ---------------------- 메인 로직 ----------------------
def generate_all_topics():
    try:
        with open(TOPIC_PATH, "r", encoding="utf-8") as f:
            topics = json.load(f).get("topics", [])
    except Exception as e:
        logging.error(f"토픽 파일 읽기 실패: {e}")
        return

    results = []
    for topic in topics:
        try:
            keywords = generate_keywords(topic)
            results.append({"topic": topic, "keywords": keywords})
            logging.info(f"{topic}: {', '.join(keywords)}")
        except Exception as e:
            logging.error(f"{topic} 키워드 생성 실패: {e}")

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump({"timestamp": datetime.utcnow().isoformat() + 'Z', "topics": results}, f, ensure_ascii=False, indent=2)
    logging.info(f"✅ 키워드 저장 완료: {OUTPUT_PATH}")

if __name__ == "__main__":
    generate_all_topics()
