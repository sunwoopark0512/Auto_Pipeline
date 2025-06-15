"""
GPT 실패 로그(JSON 리스트)에서 status=='failed' 항목만 추출.
사용: python scripts/parse_failed_gpt.py failed_log.json
"""
import json
import pathlib
import sys


def parse_fail_log(path: str) -> list[dict]:
    data = json.loads(pathlib.Path(path).read_text())
    return [item for item in data if item.get("status") == "failed"]


if __name__ == "__main__":
    print(json.dumps(parse_fail_log(sys.argv[1]), indent=2, ensure_ascii=False))
