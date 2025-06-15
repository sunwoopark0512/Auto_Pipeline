import os
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

FAILED_PATH = os.getenv('FAILED_HOOK_PATH', 'logs/failed_hooks.json')
OUTPUT_PATH = os.getenv('REPARSED_OUTPUT_PATH', 'logs/failed_keywords_reparsed.json')


def parse_failed_gpt():
    """Simple placeholder that copies FAILED_PATH to OUTPUT_PATH."""
    if not os.path.exists(FAILED_PATH):
        logging.warning("No failed hooks file found at %s", FAILED_PATH)
        return
    try:
        with open(FAILED_PATH, 'r', encoding='utf-8') as src:
            data = json.load(src)
        with open(OUTPUT_PATH, 'w', encoding='utf-8') as dst:
            json.dump(data, dst, ensure_ascii=False, indent=2)
        logging.info("Parsed failed GPT results written to %s", OUTPUT_PATH)
    except Exception as exc:
        logging.error("Error parsing failed GPT results: %s", exc)


if __name__ == '__main__':
    parse_failed_gpt()
