"""프로젝트 구조 테스트."""

import os
import pytest


EXPECTED_DIRS = ["src", "tests", "docs", "scripts"]
EXPECTED_FILES = ["fix_exporter.py", "scripts/bootstrap.sh"]


def test_directory_structure():
    for d in EXPECTED_DIRS:
        assert os.path.isdir(d), f"Missing directory: {d}"
    for f in EXPECTED_FILES:
        assert os.path.isfile(f), f"Missing file: {f}"
