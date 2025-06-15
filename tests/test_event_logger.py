from unittest import mock
from contextlib import contextmanager
from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path
import sys

bundle_dir = Path(__file__).resolve().parent.parent / "vinfinity_saas_production_bundle_v1.0"
sys.path.insert(0, str(bundle_dir))
spec = spec_from_file_location("event_logger", bundle_dir / "event_logger.py")
event_logger = module_from_spec(spec)
spec.loader.exec_module(event_logger)


def test_log_event_executes_insert():
    mock_conn = mock.MagicMock()
    mock_cursor_cm = mock.MagicMock()
    mock_cursor = mock_cursor_cm.__enter__.return_value
    mock_conn.cursor.return_value = mock_cursor_cm

    @contextmanager
    def fake_get_conn():
        yield mock_conn

    with mock.patch.object(event_logger, "get_conn", fake_get_conn):
        event_logger.log_event("user", "login", foo="bar")

    mock_cursor.execute.assert_called_once()
    mock_conn.commit.assert_called_once()
