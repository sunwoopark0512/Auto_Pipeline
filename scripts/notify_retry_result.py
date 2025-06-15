"""재시도 결과 summary(JSON)를 Slack Webhook으로 알림."""
import os, json, requests, sys

HOOK = os.getenv('SLACK_WEBHOOK', '')

def notify(summary: dict):
    if not HOOK:
        print('⚠️  SLACK_WEBHOOK 미설정 – 알림 생략')
        return
    requests.post(HOOK, json={'text': f"✅ GPT 재시도 결과
```{json.dumps(summary, indent=2, ensure_ascii=False)}```"})

if __name__ == '__main__':
    notify(json.loads(sys.stdin.read()))
