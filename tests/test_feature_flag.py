import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from unittest.mock import MagicMock, patch
from core.feature_flag import flag_enabled


def test_flag_enabled_variation_used_when_initialized():
    mock_client = MagicMock()
    mock_client.is_initialized.return_value = True
    mock_client.variation.return_value = True
    with patch("core.feature_flag.client", mock_client):
        assert flag_enabled("test-flag", "user1") is True
        mock_client.variation.assert_called_with("test-flag", {"key": "user1"}, False)


def test_flag_enabled_returns_false_when_not_initialized():
    mock_client = MagicMock()
    mock_client.is_initialized.return_value = False
    with patch("core.feature_flag.client", mock_client):
        assert flag_enabled("whatever") is False
