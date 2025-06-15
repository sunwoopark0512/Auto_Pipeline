from pathlib import Path

from ai_self_heal.rca_engine import capture_exception


def test_capture_exception(tmp_path: Path) -> None:
    log_file = tmp_path / "rca.log"
    try:
        raise RuntimeError("boom")
    except RuntimeError as exc:
        capture_exception(exc, file=log_file)

    content = log_file.read_text(encoding="utf-8")
    assert "RuntimeError" in content
    assert "boom" in content
