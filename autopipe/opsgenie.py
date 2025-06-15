import os
import requests

API_KEY = os.getenv("OPSGENIE_API_KEY")
TEAM = os.getenv("OPSGENIE_TEAM", "core")

# priority 결정 로직

def _map_priority(step: str, error: str) -> str:
    if "gpt.api" in step and ("429" in error or error.startswith("5")):
        return "P2"
    if "notion.api" in step:
        return "P3"
    return "P4"

def alert(message: str, step: str = "", error: str = "") -> None:
    if not API_KEY:
        return
    prio = _map_priority(step, error)
    body = {
        "message": message,
        "priority": prio,
        "teams": [{"name": TEAM}],
        "source": "autopipeline",
    }
    try:
        requests.post(
            "https://api.opsgenie.com/v2/alerts",
            json=body,
            headers={"Authorization": f"GenieKey {API_KEY}"},
            timeout=5,
        )
    except Exception:
        pass
