"""Tests for the Slack notifier utility."""
from unittest.mock import patch, MagicMock

import slack_notifier


def test_send_slack_message_success():
    """send_slack_message should post message payload and return status code."""
    with patch('requests.post') as mock_post:
        mock_resp = MagicMock(status_code=200)
        mock_post.return_value = mock_resp
        status = slack_notifier.send_slack_message('http://example.com', 'hello')
        mock_post.assert_called_once_with('http://example.com', json={'text': 'hello'}, timeout=10)
        assert status == 200
