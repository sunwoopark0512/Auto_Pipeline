import json
import os
import sys
from unittest.mock import patch

sys.path.insert(0, os.path.abspath("scripts"))

def test_count_results(tmp_path, monkeypatch):
    original = [{"k":1}, {"k":2}]
    still = [{"k":1}]
    fail_path = tmp_path / "orig.json"
    repath = tmp_path / "re.json"
    fail_path.write_text(json.dumps(original))
    repath.write_text(json.dumps(still))
    monkeypatch.setenv("FAILED_HOOK_PATH", str(fail_path))
    monkeypatch.setenv("REPARSED_OUTPUT_PATH", str(repath))
    from notify_retry_result import count_results
    success, failed = count_results()
    assert success == 1
    assert failed == 1

def test_notify_retry_result(tmp_path, monkeypatch):
    original = [{"k":1}]
    still = []
    fail_path = tmp_path / "orig.json"
    repath = tmp_path / "re.json"
    fail_path.write_text(json.dumps(original))
    repath.write_text(json.dumps(still))
    monkeypatch.setenv("FAILED_HOOK_PATH", str(fail_path))
    monkeypatch.setenv("REPARSED_OUTPUT_PATH", str(repath))
    monkeypatch.setenv("SLACK_WEBHOOK_URL", "http://example.com")
    from unittest.mock import patch
    import importlib
    if "notify_retry_result" in sys.modules:
        importlib.reload(sys.modules["notify_retry_result"])
    with patch("notify_retry_result.requests.post") as mock_post:
        mock_post.return_value.status_code = 200
        from notify_retry_result import notify_retry_result
        result = notify_retry_result()
        assert result == (1, 0)
        mock_post.assert_called_once()
