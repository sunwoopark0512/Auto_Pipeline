"""I/O helper functions with buffered access."""
from __future__ import annotations

import json
from typing import Any


BUFFER_SIZE = 1024 * 8


def read_json(path: str) -> Any:
    """Read JSON file using buffered IO."""
    with open(path, "r", buffering=BUFFER_SIZE) as f:
        return json.load(f)


def write_json(path: str, data: Any) -> None:
    """Write JSON to path using buffered IO."""
    with open(path, "w", buffering=BUFFER_SIZE) as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

