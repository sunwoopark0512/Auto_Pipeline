from unittest import mock
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from scripts.log_ops import build_payload, create_ops_log_entry
def test_build_payload_basic():
    payload = build_payload(
        log_type="DevOps",
        operator="tester",
        module="mod",
        environment="Local",
        task_summary="sum",
        action_details="detail",
    )
    props = payload["properties"]
    assert props["Log Type"]["select"]["name"] == "DevOps"
    assert props["Operator"]["title"][0]["text"]["content"] == "tester"
def test_create_ops_log_entry_success():
    with mock.patch("requests.post") as post:
        post.return_value.status_code = 200
        post.return_value.text = "ok"
        ok = create_ops_log_entry(
            log_type="DevOps",
            operator="tester",
            module="mod",
            environment="Local",
            task_summary="sum",
            action_details="detail",
        )
        assert ok
        post.assert_called_once()
