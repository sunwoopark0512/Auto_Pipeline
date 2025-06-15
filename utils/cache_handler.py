"""Simple file-based caching utilities."""
from __future__ import annotations

import hashlib
import json
import os
import time
from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class CacheEntry:
    value: Any
    expires_at: Optional[float] = None


class CacheHandler:
    """Cache values on disk to avoid repeated computation."""

    def __init__(self, directory: str = "cache") -> None:
        self.directory = directory
        os.makedirs(directory, exist_ok=True)

    def _path_for_key(self, key: str) -> str:
        digest = hashlib.sha256(key.encode()).hexdigest()
        return os.path.join(self.directory, f"{digest}.json")

    def get(self, key: str) -> Optional[Any]:
        path = self._path_for_key(key)
        if not os.path.exists(path):
            return None
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if data.get("expires_at") and data["expires_at"] < time.time():
            os.remove(path)
            return None
        return data["value"]

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        entry = CacheEntry(value=value)
        if ttl:
            entry.expires_at = time.time() + ttl
        path = self._path_for_key(key)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(entry.__dict__, f, ensure_ascii=False)

