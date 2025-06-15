import os
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

SUMMARY_PATH = os.getenv('REPARSED_OUTPUT_PATH', 'logs/failed_keywords_reparsed.json')


def notify_retry_result():
    """Placeholder for notifying retry results. Currently logs summary."""
    if not os.path.exists(SUMMARY_PATH):
        logging.info("No summary file found to notify: %s", SUMMARY_PATH)
        return
    try:
        with open(SUMMARY_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        count = len(data) if isinstance(data, list) else 0
        logging.info("Retry summary contains %d items", count)
    except Exception as exc:
        logging.error("Failed to read summary file: %s", exc)


if __name__ == '__main__':
    notify_retry_result()
