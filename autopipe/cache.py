"""Simple JSON backed keyword cache."""

import json
import os
from typing import Set


class KeywordCache:
    """Manage a keyword existence cache stored in JSON."""

    def __init__(self, path: str):
        self.path = path
        self._data: Set[str] = set()
        self._load()

    def _load(self) -> None:
        """Load cache file if present."""
        if os.path.exists(self.path):
            try:
                with open(self.path, "r", encoding="utf-8") as f:
                    self._data = set(json.load(f))
            except Exception:
                self._data = set()

    def exists(self, keyword: str) -> bool:
        """Return True if ``keyword`` is already cached."""
        return keyword in self._data

    def add(self, keyword: str) -> None:
        """Add ``keyword`` to the cache and persist it."""
        self._data.add(keyword)
        self._dump()

    def _dump(self) -> None:
        """Write cache contents to disk."""
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(sorted(self._data), f, ensure_ascii=False, indent=2)
