"""Utility for validating generated hook JSON files."""

import json
import sys
from pathlib import Path
from pydantic import ValidationError

from .models import HookItem


def main(path: str) -> None:
    """Validate the JSON file at ``path`` against :class:`HookItem`."""
    data = Path(path).read_text(encoding="utf-8")
    items = json.loads(data)
    if isinstance(items, dict):
        items = items.get("filtered_keywords") or items
    if not isinstance(items, list):
        print("Invalid JSON structure")
        sys.exit(1)
    for obj in items:
        try:
            HookItem(**obj)
        except ValidationError as e:
            print(f"Validation error for {obj.get('keyword')}: {e}")
            sys.exit(1)
    print("Schema validation passed")


if __name__ == "__main__":
    main(sys.argv[1])
