from unittest.mock import patch

from sla_monitor import record_sla_issue


def test_record_sla_issue_calls_clients():
    with patch("sla_monitor.NotionClient") as mock_notion, patch(
        "sla_monitor.send_slack_alert"
    ) as mock_slack:
        mock_instance = mock_notion.return_value
        mock_instance.create_page.return_value.status_code = 200
        record_sla_issue("mod", "prod", "err")
        mock_instance.create_page.assert_called_once()
        mock_slack.assert_called_once()
