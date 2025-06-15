import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from modules import generate_keywords, slack_notifier
import cli


def test_cli_generate_keywords(monkeypatch):
    calls = {}

    def fake_run():
        calls['ran'] = True
        return 'path.json'

    def fake_notify(message):
        calls['message'] = message

    monkeypatch.setattr(generate_keywords, 'run', fake_run)
    monkeypatch.setattr(slack_notifier, 'send_slack_message', fake_notify)

    cli.main(['generate_keywords', '--notify'])

    assert calls['ran'] is True
    assert 'path.json' in calls['message']
