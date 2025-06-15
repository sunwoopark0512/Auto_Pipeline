"""Opsgenie alerting helpers with step based priority routing."""

import os
import requests

ENV_TAG = os.getenv("APP_ENV", "dev")
API_KEY = os.getenv("OPSGENIE_API_KEY", "")
REGION = os.getenv("OPSGENIE_REGION", "EU")

TEAM_DEFAULT = os.getenv("OPSGENIE_TEAM", "DevOps")
TEAM_MAP = {
    "gpt": os.getenv("OPSGENIE_TEAM_GPT", "MLTeam"),
    "notion": os.getenv("OPSGENIE_TEAM_NOTION", "ContentOps"),
}

API_URL = "https://api.opsgenie.com/v2/alerts"
HEADERS = {"Authorization": f"GenieKey {API_KEY}", "Content-Type": "application/json"}


def _map_priority(step: str, error: str) -> tuple[str, str]:
    """Return Opsgenie priority and team for a given pipeline step."""

    if "gpt.api" in step and ("429" in error or error.startswith("5")):
        return "P1", TEAM_MAP["gpt"]
    if "notion.api" in step:
        return "P2", TEAM_MAP["notion"]
    return "P4", TEAM_DEFAULT


def alert(message: str, step: str = "", error: str = ""):
    """Send an Opsgenie alert with routing based on the step and error."""

    prio, team = _map_priority(step, error)
    body = {
        "message": message,
        "priority": prio,
        "teams": [{"name": team}],
        "tags": [f"env:{ENV_TAG}", f"step:{step}"],
        "source": "autopipeline",
    }
    try:
        requests.post(API_URL, json=body, headers=HEADERS, timeout=5)
    except Exception:
        pass
