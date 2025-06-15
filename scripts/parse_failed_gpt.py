import os
import json
import logging

def parse_failed_gpt():
    failed_path = os.getenv("FAILED_HOOK_PATH", "logs/failed_hooks.json")
    output_path = os.getenv("REPARSED_OUTPUT_PATH", "logs/failed_keywords_reparsed.json")
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')
    if not os.path.exists(failed_path):
        logging.warning(f"\u2757 실패 로그 파일이 존재하지 않습니다: {failed_path}")
        return
    try:
        with open(failed_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        logging.error(f"\u274c 파일 읽기 오류: {e}")
        return
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    logging.info(f"\u2705 파싱 결과 저장 완료: {output_path}")

if __name__ == "__main__":
    parse_failed_gpt()
