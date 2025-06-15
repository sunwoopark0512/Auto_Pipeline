import os
import json
import requests

SLACK = os.getenv("SLACK_WEBHOOK")

def alert(rule, evt):
    msg = f"\ud83d\udea8 *{rule['id']}* - {evt['trace_id']}\n{rule['description']}"
    if SLACK:
        requests.post(SLACK, json={"text": msg})
