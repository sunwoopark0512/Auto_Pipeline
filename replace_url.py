"""Utility script to replace remote domain references across the project."""

from __future__ import annotations

import argparse
from pathlib import Path

EXCLUDED_DIRS = {".git", "logs", "__pycache__"}


def replace_in_file(path: Path, old: str, new: str) -> bool:
    data = path.read_text()
    if old not in data:
        return False
    path.write_text(data.replace(old, new))
    return True


def scan_and_replace(root: Path, old: str, new: str) -> list[Path]:
    replaced = []
    for file_path in root.rglob("*.py"):
        if any(part in EXCLUDED_DIRS for part in file_path.parts):
            continue
        if replace_in_file(file_path, old, new):
            replaced.append(file_path)
    return replaced


def main() -> None:
    parser = argparse.ArgumentParser(description="Replace domain URLs in files")
    parser.add_argument("--old", required=True, help="Domain to replace")
    parser.add_argument("--new", required=True, help="Replacement domain")
    parser.add_argument("--root", default=".", help="Project root")
    args = parser.parse_args()

    root_dir = Path(args.root)
    files = scan_and_replace(root_dir, args.old, args.new)
    if files:
        print("Updated files:")
        for f in files:
            print(f"- {f}")
    else:
        print("No references found.")


if __name__ == "__main__":
    main()
