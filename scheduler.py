import os
import time
import logging
from datetime import datetime, timezone
import requests
import subprocess
from typing import List, Dict

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s:%(message)s')

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY')
SCHEDULE_TABLE = os.getenv('SCHEDULE_TABLE', 'content_schedule')
POLL_INTERVAL = int(os.getenv('SCHEDULE_POLL_INTERVAL', '60'))

HEADERS = {
    'apikey': SUPABASE_SERVICE_KEY or '',
    'Authorization': (
        f'Bearer {SUPABASE_SERVICE_KEY}' if SUPABASE_SERVICE_KEY else ''
    ),
}


def fetch_pending_tasks() -> List[Dict]:
    if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
        logging.error('SUPABASE_URL or SUPABASE_SERVICE_KEY missing')
        return []
    url = f"{SUPABASE_URL}/rest/v1/{SCHEDULE_TABLE}?status=eq.pending&select=*"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        logging.error('Failed to fetch tasks: %s', e)
        return []


def update_task_status(task_id: int, status: str) -> None:
    url = f"{SUPABASE_URL}/rest/v1/{SCHEDULE_TABLE}?id=eq.{task_id}"
    data = {'status': status}
    try:
        requests.patch(
            url,
            json=data,
            headers={**HEADERS, 'Prefer': 'return=representation'},
            timeout=10,
        )
    except Exception as e:
        logging.warning('Failed to update status for %s: %s', task_id, e)


def run_upload_pipeline() -> bool:
    try:
        result = subprocess.run([
            'python', 'run_pipeline.py'
        ], capture_output=True, text=True)
        if result.returncode == 0:
            logging.info('Pipeline run succeeded')
            return True
        logging.error('Pipeline failed: %s', result.stderr)
        return False
    except Exception as e:
        logging.error('Pipeline execution error: %s', e)
        return False


def process_task(task: Dict) -> None:
    task_id = task.get('id')
    if task_id is None:
        logging.warning('Task without id skipped')
        return
    scheduled = task.get('scheduled_time')
    if scheduled:
        try:
            scheduled_dt = datetime.fromisoformat(
                scheduled.replace('Z', '+00:00')
            )
            if scheduled_dt > datetime.now(timezone.utc):
                return
        except ValueError:
            logging.warning('Invalid scheduled_time for task %s', task_id)
    update_task_status(task_id, 'processing')
    success = run_upload_pipeline()
    update_task_status(task_id, 'complete' if success else 'failed')


def run_scheduler() -> None:
    logging.info('Scheduler started')
    while True:
        tasks = fetch_pending_tasks()
        for task in tasks:
            process_task(task)
        time.sleep(POLL_INTERVAL)


if __name__ == '__main__':
    run_scheduler()
