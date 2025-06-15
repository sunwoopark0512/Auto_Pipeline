import json
import os
import sys
import types

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
dummy_client = types.SimpleNamespace()
dummy_client.Client = lambda *args, **kwargs: object()
sys.modules.setdefault('notion_client', dummy_client)
os.makedirs('logs', exist_ok=True)


def test_notify_retry_result(monkeypatch, tmp_path):
    result_file = tmp_path / "result.json"
    data = [
        {"keyword": "a"},
        {"keyword": "b", "retry_error": "err"}
    ]
    result_file.write_text(json.dumps(data, ensure_ascii=False))

    calls = {}

    class DummyResponse:
        status = 200
        def read(self):
            return b"ok"

    def dummy_urlopen(req):
        calls['req'] = req
        return DummyResponse()

    monkeypatch.setenv("REPARSED_OUTPUT_PATH", str(result_file))
    monkeypatch.setenv("SLACK_WEBHOOK_URL", "http://example.com")
    from scripts import notify_retry_result  # import after env setup
    monkeypatch.setattr(notify_retry_result.urllib.request, 'urlopen', dummy_urlopen)

    notify_retry_result.notify_retry_result()

    assert calls
    payload = json.loads(calls['req'].data.decode())
    assert "총 시도: 2" in payload['text']
    assert "성공: 1" in payload['text']
    assert "실패: 1" in payload['text']
