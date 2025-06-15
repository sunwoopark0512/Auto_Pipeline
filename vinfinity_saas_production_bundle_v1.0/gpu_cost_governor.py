import os, time
from slack_notifier import send_slack_message
from utils.init_env import load_env

env = load_env()

HARD_BUDGET_HOURS = float(os.getenv("GPU_MONTHLY_HRS", "100"))
SENT = False

def gpu_hours_consumed() -> float:
    return float(open("/var/log/gpu_usage.txt").read().strip())

while True:
    used = gpu_hours_consumed()
    if used > HARD_BUDGET_HOURS and not SENT:
        send_slack_message(env["SLACK_WEBHOOK"], f"\ud83d\udea8 GPU budget exceeded: {used}h")
        SENT = True
    time.sleep(3600)
