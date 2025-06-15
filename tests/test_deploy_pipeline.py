from unittest.mock import patch

from deploy_pipeline import run_deployment_pipeline


def test_run_deployment_pipeline():
    with patch("deploy_pipeline.auto_deployment_log") as mock_log, patch(
        "deploy_pipeline.send_slack_alert"
    ) as mock_slack:
        run_deployment_pipeline("mod", "prod", "v1")
        mock_log.assert_called_once()
        mock_slack.assert_called_once()
