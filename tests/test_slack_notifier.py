import os
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from modules import slack_notifier


def test_send_slack_message(monkeypatch):
    sent = {}

    def fake_post(url, json, timeout):
        sent['url'] = url
        sent['json'] = json
        class R:
            status_code = 200
            text = ''
        return R()

    monkeypatch.setattr(slack_notifier.requests, 'post', fake_post)
    os.environ['SLACK_WEBHOOK_URL'] = 'http://example.com/webhook'
    slack_notifier.send_slack_message('hello')
    assert sent['url'] == 'http://example.com/webhook'
    assert sent['json'] == {'text': 'hello'}
