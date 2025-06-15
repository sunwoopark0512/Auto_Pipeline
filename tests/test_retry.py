import pytest
from autopipe.retry import gpt_retry


calls = {
    "count": 0,
}

@gpt_retry()
def flaky():
    calls["count"] += 1
    if calls["count"] < 2:
        raise ValueError("fail")
    return "ok"

def test_gpt_retry():
    assert flaky() == "ok"
    assert calls["count"] == 2
