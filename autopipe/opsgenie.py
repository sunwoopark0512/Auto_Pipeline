import os
import requests

API_KEY = os.getenv("OPSGENIE_API_KEY")
TEAM = os.getenv("OPSGENIE_TEAM", "DevOps")
REGION = os.getenv("OPSGENIE_REGION", "US").upper()
BASE = "https://api.eu.opsgenie.com" if REGION == "EU" else "https://api.opsgenie.com"
ENV_TAG = os.getenv("APP_ENV", "prod")


def notify(message: str, prio: str = "P3") -> None:
    hdr = {"Authorization": f"GenieKey {API_KEY}"}
    body = {
        "message": message,
        "priority": prio,
        "teams": [{"name": TEAM}],
        "tags": [f"env:{ENV_TAG}"],
        "source": "autopipeline",
    }
    requests.post(f"{BASE}/v2/alerts", json=body, headers=hdr, timeout=5)
