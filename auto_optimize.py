import os
import logging
import requests

from logging_config import setup_logging

setup_logging()

AD_API_ENDPOINT = "https://ads.example.com/optimize"


def call_ads_api(payload):
    response = requests.post(AD_API_ENDPOINT, json=payload, timeout=5)
    response.raise_for_status()
    return response.json()


def main():
    dry_run = os.getenv("DRY_RUN", "false").lower() == "true"
    if dry_run:
        logging.info("DRY_RUN enabled - skipping ad API call")
        return

    payload = {"sample": "data"}
    try:
        result = call_ads_api(payload)
        logging.info("Ads API result: %s", result)
    except Exception as e:
        logging.error("Ads API call failed: %s", e)
        raise


if __name__ == "__main__":
    main()
