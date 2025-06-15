"""CLI tools for manual maintenance operations."""
from __future__ import annotations

from pathlib import Path
import argparse
import logging

from .cache_handler import CacheHandler


def clear_cache(directory: str) -> None:
    handler = CacheHandler(directory)
    for file in list(Path(directory).glob("*.json")):
        file.unlink()
    logging.info("Cache directory %s cleared", directory)


def main() -> None:
    parser = argparse.ArgumentParser(description="Manual maintenance utilities")
    parser.add_argument("command", choices=["clear-cache"])
    parser.add_argument("--cache-dir", default="cache")
    args = parser.parse_args()

    if args.command == "clear-cache":
        clear_cache(args.cache_dir)


if __name__ == "__main__":
    main()

