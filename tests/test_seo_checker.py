import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from seo import check_seo


def test_check_seo(tmp_path):
    file_a = tmp_path / "a.txt"
    file_a.write_text("content")
    check_seo([str(file_a)])
