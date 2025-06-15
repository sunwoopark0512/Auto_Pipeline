from ops_log_model import OpsLogModel


def test_build_payload_contains_properties():
    payload = OpsLogModel.build_payload(
        log_type="Deploy",
        operator="tester",
        module="mod",
        environment="prod",
        task_summary="summary",
        action_details="details",
        status="성공",
    )
    assert "properties" in payload
    props = payload["properties"]
    assert props["모듈"]["title"][0]["text"]["content"] == "mod"
