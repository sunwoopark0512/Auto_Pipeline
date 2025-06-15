from fastapi.testclient import TestClient
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from webhook_receiver import app  # noqa: E402

client = TestClient(app)


def test_health():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "alive"}


def test_invalid_secret():
    payload = {"secret": "wrong", "command": "orchestrator"}
    res = client.post("/webhook/", json=payload)
    assert res.status_code == 401


def test_invalid_command():
    payload = {"secret": "supersecret", "command": "unknown"}
    res = client.post("/webhook/", json=payload)
    assert res.status_code == 400
