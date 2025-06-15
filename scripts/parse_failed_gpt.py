import os
import json
import logging

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')
    src = os.getenv("FAILED_HOOK_PATH", "logs/failed_hooks.json")
    dst = os.getenv("REPARSED_OUTPUT_PATH", "logs/failed_keywords_reparsed.json")
    if not os.path.exists(src):
        logging.warning(f"Input not found: {src}")
        return
    with open(src, 'r', encoding='utf-8') as f:
        data = json.load(f)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with open(dst, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    logging.info(f"Parsed failed GPT output -> {dst}")

if __name__ == "__main__":
    main()
