import logging
from logging_config import setup_logging


def test_logging_fields(caplog):
    setup_logging()
    logger = logging.getLogger("test")
    with caplog.at_level(logging.INFO):
        logger.info("msg")
    assert caplog.records
    rec = caplog.records[0]
    assert hasattr(rec, "dd.trace_id") and hasattr(rec, "dd.span_id")
