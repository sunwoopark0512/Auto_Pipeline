import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from utils.auth import verify_slack_signature
from flask import Request
from werkzeug.test import EnvironBuilder
import hashlib
import hmac


def make_request(body: str, secret: str, timestamp: str) -> Request:
    builder = EnvironBuilder(method="POST", data=body)
    env = builder.get_environ()
    env["HTTP_X_SLACK_REQUEST_TIMESTAMP"] = timestamp
    sig_basestring = f"v0:{timestamp}:{body}"
    signature = "v0=" + hmac.new(secret.encode(), sig_basestring.encode(), hashlib.sha256).hexdigest()
    env["HTTP_X_SLACK_SIGNATURE"] = signature
    return Request(env)


def test_verify_slack_signature_valid(monkeypatch):
    secret = "test_secret"
    os.environ["SLACK_SIGNING_SECRET"] = secret
    body = "command=/vinfo"
    timestamp = "1000"

    monkeypatch.setattr("time.time", lambda: 1000)
    req = make_request(body, secret, timestamp)
    assert verify_slack_signature(req)


def test_verify_slack_signature_invalid(monkeypatch):
    secret = "test_secret"
    os.environ["SLACK_SIGNING_SECRET"] = secret
    body = "command=/vinfo"
    timestamp = "1000"

    monkeypatch.setattr("time.time", lambda: 2000)
    req = make_request(body, secret, timestamp)
    assert not verify_slack_signature(req)
