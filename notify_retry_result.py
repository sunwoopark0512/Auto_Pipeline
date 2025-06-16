import os
import json
import logging

RESULT_PATH = os.getenv("REPARSED_OUTPUT_PATH", "logs/failed_keywords_reparsed.json")

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

def main():
    if not os.path.exists(RESULT_PATH):
        logging.info(f"❗ 결과 파일이 존재하지 않습니다: {RESULT_PATH}")
        return

    with open(RESULT_PATH, 'r', encoding='utf-8') as f:
        items = json.load(f)

    failed = len([i for i in items if i.get("retry_error")])
    success = len(items) - failed
    logging.info(f"🔔 재시도 결과 - 성공: {success} | 실패: {failed}")
    print(json.dumps({"success": success, "failed": failed}))

if __name__ == "__main__":
    main()
