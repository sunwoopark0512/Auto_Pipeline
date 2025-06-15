"""User input validation helpers."""
from __future__ import annotations

import json
import re
from typing import Any, Optional

SCRIPT_PATTERN = re.compile(r"<\/??script.*?>", re.IGNORECASE)
SQL_PATTERN = re.compile(r"(--|;)|\b(OR|AND)\b.*=", re.IGNORECASE)


def sanitize_text(text: str) -> str:
    """Remove potentially dangerous substrings."""
    text = SCRIPT_PATTERN.sub("", text)
    text = SQL_PATTERN.sub("", text)
    return text


def parse_json(text: str) -> Optional[Any]:
    """Parse JSON safely, returning None on error."""
    try:
        return json.loads(text)
    except Exception:
        return None


