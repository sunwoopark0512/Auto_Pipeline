import os
import json
import logging

REPARSED_PATH = os.getenv("REPARSED_OUTPUT_PATH", "logs/failed_keywords_reparsed.json")

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

def notify() -> int:
    if not os.path.exists(REPARSED_PATH):
        logging.warning(f"❗ 재시도 결과 파일이 없습니다: {REPARSED_PATH}")
        return 0

    with open(REPARSED_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    total = len(data)
    failed = len([d for d in data if d.get("retry_error")])
    success = total - failed

    logging.info(f"📢 재시도 결과 - 총 {total}, 성공 {success}, 실패 {failed}")
    return total

if __name__ == "__main__":
    notify()
