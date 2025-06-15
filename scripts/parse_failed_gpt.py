import os
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

FAILED_PATH = os.getenv("FAILED_HOOK_PATH", "logs/failed_hooks.json")


def parse_failed_gpt():
    if not os.path.exists(FAILED_PATH):
        logging.info(f"No failed GPT results found at {FAILED_PATH}")
        return

    with open(FAILED_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    logging.info(f"Found {len(data)} failed GPT items")
    for item in data:
        logging.debug(item)


if __name__ == "__main__":
    parse_failed_gpt()
