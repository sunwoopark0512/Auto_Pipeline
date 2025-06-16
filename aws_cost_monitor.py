import os
import logging
from datetime import datetime

import boto3
import requests
from dotenv import load_dotenv

# ---------------------- 설정 로딩 ----------------------
load_dotenv()
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
AWS_COST_THRESHOLD = float(os.getenv("AWS_COST_THRESHOLD", "100"))

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

# ---------------------- AWS 비용 조회 함수 ----------------------
def get_monthly_cost():
    ce = boto3.client('ce')
    now = datetime.utcnow()
    start = now.replace(day=1).strftime('%Y-%m-%d')
    end = now.strftime('%Y-%m-%d')

    response = ce.get_cost_and_usage(
        TimePeriod={'Start': start, 'End': end},
        Granularity='MONTHLY',
        Metrics=['UnblendedCost']
    )

    amount = response['ResultsByTime'][0]['Total']['UnblendedCost']['Amount']
    return float(amount)

# ---------------------- 슬랙 알림 함수 ----------------------
def send_slack_alert(cost, threshold):
    if not SLACK_WEBHOOK_URL:
        logging.error("SLACK_WEBHOOK_URL 환경 변수가 설정되어 있지 않습니다.")
        return

    now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    message = (
        f"AWS 월간 비용 경고!\n"
        f"현재 비용: ${cost:.2f}\n"
        f"임계값: ${threshold:.2f}\n"
        f"시각: {now} UTC"
    )
    try:
        requests.post(SLACK_WEBHOOK_URL, json={'text': message})
        logging.info("슬랙 알림 전송 완료")
    except Exception as e:
        logging.error(f"슬랙 알림 전송 실패: {e}")

# ---------------------- 메인 ----------------------
if __name__ == "__main__":
    try:
        cost = get_monthly_cost()
        logging.info(f"월 누적 비용: ${cost:.2f} (임계값 ${AWS_COST_THRESHOLD:.2f})")
        if cost > AWS_COST_THRESHOLD:
            send_slack_alert(cost, AWS_COST_THRESHOLD)
        else:
            logging.info("비용이 임계값 이하입니다.")
    except Exception as e:
        logging.error(f"AWS 비용 확인 실패: {e}")
