import os
import logging
from datetime import datetime

import boto3
from dotenv import load_dotenv

# ---------------------- 환경 변수 로딩 ----------------------
load_dotenv()
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_SESSION_TOKEN = os.getenv("AWS_SESSION_TOKEN")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

# ---------------------- 로깅 설정 ----------------------
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

# ---------------------- AWS Cost Explorer 클라이언트 ----------------------
if not AWS_ACCESS_KEY_ID or not AWS_SECRET_ACCESS_KEY:
    logging.error("❗ AWS 인증 정보(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)가 누락되었습니다.")
    exit(1)

ce = boto3.client(
    "ce",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    aws_session_token=AWS_SESSION_TOKEN,
)

# ---------------------- 월별 비용 조회 ----------------------
def log_current_month_cost():
    today = datetime.utcnow().date()
    start = today.replace(day=1)
    # 다음 달 첫 날 계산
    if start.month == 12:
        next_month = start.replace(year=start.year + 1, month=1)
    else:
        next_month = start.replace(month=start.month + 1)

    resp = ce.get_cost_and_usage(
        TimePeriod={"Start": start.strftime("%Y-%m-%d"), "End": next_month.strftime("%Y-%m-%d")},
        Granularity="MONTHLY",
        Metrics=["UnblendedCost"],
    )

    total = resp["ResultsByTime"][0]["Total"]["UnblendedCost"]
    amount = total.get("Amount")
    unit = total.get("Unit")
    logging.info(f"💰 AWS 비용 {start.strftime('%Y-%m')}: {amount} {unit}")


if __name__ == "__main__":
    log_current_month_cost()
