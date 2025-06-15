import os
from utils.logger import setup_logger

def test_setup_logger_file(tmp_path, monkeypatch):
    log_path = tmp_path / "test.log"
    monkeypatch.setenv("LOG_TO_FILE", "1")
    monkeypatch.setenv("LOG_FILE_PATH", str(log_path))

    logger = setup_logger("test_file")
    logger.info("hello")
    for handler in logger.handlers:
        handler.flush()

    assert log_path.exists()
    content = log_path.read_text()
    assert "hello" in content

