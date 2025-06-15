import re
from typing import List

COPYRIGHT_PATTERN = re.compile(r"(©|\(c\))\s?\d{4}")


def detect_copyright(text: str) -> List[str]:
    """Detect possible copyright statements in text."""
    return COPYRIGHT_PATTERN.findall(text)
