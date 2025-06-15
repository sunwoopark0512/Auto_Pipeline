import hashlib
import hmac
import os
import time
from flask import Request


def verify_slack_signature(request: Request) -> bool:
    slack_signing_secret = os.getenv("SLACK_SIGNING_SECRET")
    timestamp = request.headers.get("X-Slack-Request-Timestamp")
    if not slack_signing_secret or not timestamp:
        return False

    # 방어적 조치: 재생 공격 방지 (5분 허용)
    if abs(time.time() - int(timestamp)) > 60 * 5:
        return False

    sig_basestring = f"v0:{timestamp}:{request.get_data(as_text=True)}"
    my_signature = "v0=" + hmac.new(
        slack_signing_secret.encode(),
        sig_basestring.encode(),
        hashlib.sha256,
    ).hexdigest()
    slack_signature = request.headers.get("X-Slack-Signature")
    if not slack_signature:
        return False
    return hmac.compare_digest(my_signature, slack_signature)
