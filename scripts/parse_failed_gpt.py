"""GPT 실패 로그(JSON)에서 status=='failed' 항목만 추출."""
import json, pathlib, sys

def parse_fail_log(path: str):
    data = json.loads(pathlib.Path(path).read_text())
    return [item for item in data if item.get('status') == 'failed']

if __name__ == '__main__':
    print(json.dumps(parse_fail_log(sys.argv[1]), indent=2, ensure_ascii=False))
