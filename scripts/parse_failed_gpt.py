import os
import json
import logging
from dotenv import load_dotenv

load_dotenv()

FAILED_HOOK_PATH = os.getenv("FAILED_HOOK_PATH", "logs/failed_hooks.json")
REPARSED_OUTPUT_PATH = os.getenv("REPARSED_OUTPUT_PATH", "logs/failed_keywords_reparsed.json")

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')


def parse_failed_gpt():
    if not os.path.exists(FAILED_HOOK_PATH):
        logging.info(f"❌ 실패 파일이 존재하지 않습니다: {FAILED_HOOK_PATH}")
        return

    with open(FAILED_HOOK_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 현재는 단순 복사하여 재시도용 파일 생성
    os.makedirs(os.path.dirname(REPARSED_OUTPUT_PATH), exist_ok=True)
    with open(REPARSED_OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    logging.info(f"✅ 재시도 파일 저장 완료: {REPARSED_OUTPUT_PATH}")


if __name__ == "__main__":
    parse_failed_gpt()
