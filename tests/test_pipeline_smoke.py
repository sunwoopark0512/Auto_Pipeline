import importlib
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))


def test_imports():
    """핵심 모듈 임포트가 깨지지 않는지만 확인."""
    for module in (
        "keyword_generator",
        "content_writer",
        "editor_seo_optimizer",
        "qa_filter",
        "run_pipeline",
    ):
        assert importlib.import_module(module)
