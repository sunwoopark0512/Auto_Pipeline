#!/usr/bin/env python3
"""프로젝트 파일 자동 생성 스크립트."""

from pathlib import Path


REQUIRED_DIRS = ["src", "tests", "docs", "scripts"]
REQUIRED_FILES = ["scripts/bootstrap.sh", "requirements.txt", ".gitignore"]


def create_structure() -> None:
    """Ensure that required directories and placeholder files exist."""
    for d in REQUIRED_DIRS:
        Path(d).mkdir(exist_ok=True)
    Path("src/__init__.py").touch(exist_ok=True)
    Path("tests/__init__.py").touch(exist_ok=True)


def verify_files() -> bool:
    """Check that key files exist."""
    missing = [f for f in REQUIRED_FILES if not Path(f).exists()]
    if missing:
        print("Missing files:", ", ".join(missing))
        return False
    return True


def main() -> int:
    """Create project structure and verify required files."""
    create_structure()
    if not verify_files():
        return 1
    print("Project structure verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
