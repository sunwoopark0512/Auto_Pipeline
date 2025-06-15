"""SEO checker stub."""

from __future__ import annotations

from pathlib import Path
from typing import List


def check_seo(paths: List[str]) -> None:
    """Pretend to check SEO rules on the given paths."""
    for path in paths:
        path_obj = Path(path)
        if not path_obj.exists():
            raise FileNotFoundError(f"Path does not exist: {path}")
        # Placeholder for SEO checks
        print(f"Checking SEO for {path}")
