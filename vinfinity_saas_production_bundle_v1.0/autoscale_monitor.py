import os
import time
import psutil
import requests
from slack_notifier import send_slack_message
from utils.init_env import load_env

env = load_env()

CPU_HIGH = float(os.getenv("CPU_HIGH", "0.8"))
CPU_LOW = float(os.getenv("CPU_LOW", "0.3"))
CHECK_SEC = int(os.getenv("SCALE_INTERVAL_SEC", "60"))


def scale_service(delta: int) -> None:
    render_service_id = os.getenv("RENDER_SERVICE_ID", "")
    render_api = f"https://api.render.com/v1/services/{render_service_id}"
    headers = {"Authorization": f"Bearer {os.getenv('RENDER_API_KEY', '')}"}
    requests.post(render_api + ("/scale/up" if delta > 0 else "/scale/down"), headers=headers)


while True:
    cpu = psutil.cpu_percent() / 100
    if cpu > CPU_HIGH:
        scale_service(+1)
        send_slack_message(env["SLACK_WEBHOOK"], f"⬆️ Auto-scale UP (CPU {cpu:.0%})")
    elif cpu < CPU_LOW:
        scale_service(-1)
        send_slack_message(env["SLACK_WEBHOOK"], f"⬇️ Auto-scale DOWN (CPU {cpu:.0%})")
    time.sleep(CHECK_SEC)
