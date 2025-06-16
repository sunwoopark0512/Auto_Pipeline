#!/usr/bin/env python3
"""
content_scheduler.py
- Notion DB의 'Publish Schedule' 정보를 읽어 예약 시간에 자동 발행
- 즉시 실행 또는 Dry-Run 모드 지원
"""

import os
import json
import requests
import time
import sched
from datetime import datetime, timezone
from publish_automation import automate_publish  # 모듈 ⑦ 재사용

NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_SCHED_DB_ID = os.getenv("NOTION_SCHED_DB_ID")  # 발행 일정 DB
HEADERS = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

SCHED = sched.scheduler(time.time, time.sleep)


def fetch_scheduled_posts() -> list:
    """발행 예정 콘텐츠(미발행 상태) 조회"""
    url = f"https://api.notion.com/v1/databases/{NOTION_SCHED_DB_ID}/query"
    payload = {
        "filter": {
            "and": [
                {"property": "Status", "select": {"equals": "Scheduled"}},
                {
                    "property": "Publish\u00a0Time",
                    "date": {"after": datetime.utcnow().isoformat()},
                },
            ]
        }
    }
    res = requests.post(url, headers=HEADERS, json=payload)
    res.raise_for_status()
    return res.json()["results"]


def mark_as_published(page_id: str):
    """발행 완료 후 Status 필드를 Published 로 변경"""
    url = f"https://api.notion.com/v1/pages/{page_id}"
    payload = {"properties": {"Status": {"select": {"name": "Published"}}}}
    requests.patch(url, headers=HEADERS, json=payload)


def publish_job(page: dict, dry_run: bool = False):
    """예약한 시점에 호출되는 실제 발행 로직"""
    title = page["properties"]["Title"]["title"][0]["text"]["content"]
    content = page["properties"]["Content"]["rich_text"][0]["text"]["content"]
    platform = page["properties"]["Platform"]["select"]["name"]

    print(f"\ud83d\udd52 {datetime.utcnow().isoformat()} \u2192 \ubc1c\ud589 \uc2e4\ud589: {title} \u2192 {platform}")
    if not dry_run:
        success = automate_publish(content, title, platform=platform.lower())
        if success:
            mark_as_published(page["id"])


def schedule_posts(dry_run: bool = False):
    pages = fetch_scheduled_posts()
    if not pages:
        print("\ud83d\udced \uc608\uc815\ub41c \uac8c\uc2dc\ubb3c\uc774 \uc5c6\uc2b5\ub2c8\ub2e4.")
        return

    for p in pages:
        publish_time = p["properties"]["Publish\u00a0Time"]["date"]["start"]
        publish_dt = datetime.fromisoformat(publish_time.rstrip("Z")).replace(
            tzinfo=timezone.utc
        )
        delay = (
            publish_dt
            - datetime.utcnow().replace(tzinfo=timezone.utc)
        ).total_seconds()
        delay = max(delay, 0)

        SCHED.enter(delay, 1, publish_job, argument=(p, dry_run))
        title = p["properties"]["Title"]["title"][0]["text"]["content"]
        print(f"\u23f0 \uc608\uc815 \ub4f1\ub85d: {title} \u2192 {publish_dt}")

    print("\ud83d\ude80 \uc2a4\ucf00\uc904\ub7ec \uac00\ub3d9\u2026")
    SCHED.run()


if __name__ == "__main__":
    import argparse

    argp = argparse.ArgumentParser(description="Content Scheduler")
    argp.add_argument("--dry-run", action="store_true", help="\ubc1c\ud589 \uc5c6\uc774 \uc608\uc815 \ud655\uc778\ub9cc \uc218\ud589")
    args = argp.parse_args()

    schedule_posts(dry_run=args.dry_run)
