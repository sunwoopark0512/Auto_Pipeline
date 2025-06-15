import subprocess
import time


LOG_PATH = "logs/rca.log"
FAIL_THRESHOLD = 10
SLEEP_SEC = 600


while True:
    try:
        out = subprocess.getoutput(f"grep ERROR {LOG_PATH} | wc -l")
        if int(out) > FAIL_THRESHOLD:
            print("Multiple failures detected - Canary rollback")
            subprocess.run(["python", "infra/canary_router.py", "--rollback"], check=False)
    except Exception as exc:
        print(f"Monitor error: {exc}")
    time.sleep(SLEEP_SEC)
