"""Failure Replay Buffer utilities."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Mapping

REPLAY_PATH = Path("training/replay_buffer.jsonl")
REPLAY_PATH.parent.mkdir(parents=True, exist_ok=True)


def save_failure(sample: Mapping[str, object], path: Path = REPLAY_PATH) -> None:
    """Append a failure sample to the replay buffer."""
    with path.open("a", encoding="utf-8") as file:
        file.write(json.dumps(sample, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    SAMPLE = {"prompt": "Generate bad output", "completion": None, "error": "RateLimitError"}
    save_failure(SAMPLE)
