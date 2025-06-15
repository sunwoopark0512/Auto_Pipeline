import os
import json

import psycopg2
import stripe
from flask import Flask, request

app = Flask(__name__)
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET")


def update_user_plan(user_id, plan):
    conn = psycopg2.connect(...)
    cur = conn.cursor()
    cur.execute("UPDATE user_profiles SET plan=%s WHERE id=%s", (plan, user_id))
    conn.commit()
    cur.close()
    conn.close()


@app.route("/stripe", methods=["POST"])
def stripe_handler():
    sig = request.headers["Stripe-Signature"]
    payload = request.data.decode("utf-8")
    event = stripe.Webhook.construct_event(payload, sig, endpoint_secret)

    if event["type"] == "customer.subscription.updated":
        sub = event["data"]["object"]
        user_id = sub["metadata"]["supabase_uid"]
        plan = sub["plan"]["nickname"].lower()
        update_user_plan(user_id, plan)
    return "", 200
