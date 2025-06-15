import os
import time
import subprocess
from typing import Optional

import requests  # type: ignore[import-untyped]

PHOENIX_API = os.getenv("PHOENIX_DRIFT_API", "http://phoenix:6006/api/drift")
RETRAIN_THRESHOLD = float(os.getenv("RETRAIN_THRESHOLD", 0.3))
CHECK_INTERVAL = int(os.getenv("DRIFT_CHECK_INTERVAL", 3600))


def fetch_drift(api_url: str = PHOENIX_API) -> Optional[float]:
    """Fetch drift value from Phoenix API."""
    try:
        response = requests.get(api_url, timeout=5)
        response.raise_for_status()
        return response.json().get("value", 0.0)
    except requests.RequestException:
        return None


def handle_drift(drift: float) -> None:
    """Trigger retraining and canary rollout when drift exceeds threshold."""
    if drift > RETRAIN_THRESHOLD:
        print("⚠ Drift exceeded. Launching retraining...")
        subprocess.run(["python", "ml/rlhf_train.py"], check=False)
        subprocess.run(["python", "infra/canary_router.py"], check=False)


def main() -> None:
    """Continuous drift monitoring loop."""
    while True:
        drift = fetch_drift()
        if drift is not None:
            print(f"Drift: {drift:.2f}")
            handle_drift(drift)
        else:
            print("Failed to fetch drift data")
        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
