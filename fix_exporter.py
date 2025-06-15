#!/usr/bin/env python3
"""프로젝트 파일 자동 생성 스크립트."""

import sys
import argparse
from pathlib import Path
from typing import Dict, List

class ProjectSetup:
    """프로젝트 설정을 관리하는 클래스."""

    def __init__(self) -> None:
        """초기화."""
        self.root_dir = Path.cwd()
        self.directories: List[str] = [
            "src/",
            "tests/",
            "docs/",
            "scripts/",
        ]
        self.files: Dict[str, str] = {
            "src/__init__.py": "",
            "src/py.typed": "",
            "tests/__init__.py": "",
            "tests/conftest.py": self._get_conftest_content(),
            "tests/test_structure.py": self._get_test_content(),
            "mypy.ini": self._get_mypy_content(),
            "setup.cfg": self._get_setup_cfg_content(),
            "pytest.ini": self._get_pytest_content(),
        }

    @staticmethod
    def _get_conftest_content() -> str:
        return """
import sys
from pathlib import Path

# src 디렉토리를 Python path에 추가
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))
"""

    @staticmethod
    def _get_test_content() -> str:
        return """
from pathlib import Path

def test_project_structure():
    '프로젝트 구조를 검증합니다.'
    required_dirs = ['src', 'tests', 'docs', 'scripts']
    for directory in required_dirs:
        assert Path(directory).exists(), f"{directory} 디렉토리가 없습니다"

def test_type_hints():
    'Type hints 지원을 검증합니다.'
    assert Path('src/py.typed').exists(), 'Type hints 지원 파일이 없습니다'
"""

    @staticmethod
    def _get_mypy_content() -> str:
        return """
[mypy]
python_version = 3.11
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True
disallow_incomplete_defs = True
check_untyped_defs = True
disallow_untyped_decorators = True
no_implicit_optional = True
warn_redundant_casts = True
warn_unused_ignores = True
warn_no_return = True
warn_unreachable = True

[mypy-tests.*]
disallow_untyped_defs = False
"""

    @staticmethod
    def _get_setup_cfg_content() -> str:
        return """
[metadata]
name = your-project-name
version = 0.1.0
description = Your project description
author = sunwoopark0512

[options]
package_dir =
    = src
packages = find:
python_requires = >=3.11
install_requires =
    # 의존성을 여기에 추가하세요

[options.packages.find]
where = src

[options.extras_require]
dev =
    pytest>=7.0.0
    pytest-cov>=4.0.0
    mypy>=1.0.0
    pylint>=2.17.0
    types-setuptools

[pylint]
max-line-length = 100
disable = C0111,C0103
"""

    @staticmethod
    def _get_pytest_content() -> str:
        return """
[pytest]
testpaths = tests
python_files = test_*.py
addopts = -v --cov=src --cov-report=xml
"""

    def create_structure(self) -> None:
        """프로젝트 구조를 생성합니다."""
        for directory in self.directories:
            path = self.root_dir / directory
            path.mkdir(parents=True, exist_ok=True)
            print(f"Created directory: {directory}")

        for file_path, content in self.files.items():
            path = self.root_dir / file_path
            path.parent.mkdir(parents=True, exist_ok=True)
            if not path.exists():
                path.write_text(content.strip() + "\n")
                print(f"Created file: {file_path}")

    def verify_structure(self) -> bool:
        """프로젝트 구조를 검증합니다."""
        success = True
        for directory in self.directories:
            if not (self.root_dir / directory).exists():
                print(f"Missing directory: {directory}", file=sys.stderr)
                success = False

        for file_path in self.files:
            if not (self.root_dir / file_path).exists():
                print(f"Missing file: {file_path}", file=sys.stderr)
                success = False

        return success


def main() -> int:
    """메인 실행 함수."""
    parser = argparse.ArgumentParser(description="프로젝트 파일 생성/검증 도구")
    parser.add_argument("--verify", action="store_true", help="프로젝트 구조만 검증")
    args = parser.parse_args()

    setup = ProjectSetup()

    if args.verify:
        return 0 if setup.verify_structure() else 1

    try:
        setup.create_structure()
        print("Project structure created successfully!")
        return 0
    except Exception as e:
        print(f"Error creating project structure: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
