"""Simple Root Cause Analysis logging utility."""
from __future__ import annotations

import datetime
import traceback
from pathlib import Path
from typing import TextIO

LOG_FILE = Path("logs/rca.log")
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)


def capture_exception(exc: Exception, file: Path = LOG_FILE) -> None:
    """Append exception details and traceback to a log file."""
    timestamp = datetime.datetime.utcnow().isoformat()
    with file.open("a", encoding="utf-8") as fh:
        fh.write(f"\n[{timestamp}] {type(exc).__name__}: {exc}\n")
        fh.write(traceback.format_exc())


if __name__ == "__main__":
    try:
        raise ValueError("Sample error for RCA")
    except Exception as err:  # noqa: BLE001
        capture_exception(err)
