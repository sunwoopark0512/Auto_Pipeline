"""
예시: 실패 단계 목록을 슬랙 대시보드로 보내 재시도 트리거.
"""

from __future__ import annotations

import os
from slack_sdk.webhook import WebhookClient

_WEBHOOK = WebhookClient(os.getenv("SLACK_WEBHOOK_URL", ""))


def main(failures: list[str]):
    if not failures or not _WEBHOOK.url:
        return
    _WEBHOOK.send(
        text=f":warning: Pipeline failures: {', '.join(failures)}",
    )
