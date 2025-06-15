import pytest
from utils import retry_with_backoff

def test_retry_with_backoff_retries():
    calls = []
    def fn():
        calls.append(1)
        raise ValueError("fail")
    with pytest.raises(ValueError):
        retry_with_backoff(fn, max_retries=3, base_delay=0)
    assert len(calls) == 3

def test_retry_with_backoff_success():
    counter = {"n": 0}
    def fn():
        counter["n"] += 1
        if counter["n"] < 2:
            raise ValueError("fail")
        return "ok"
    result = retry_with_backoff(fn, max_retries=3, base_delay=0)
    assert result == "ok"
    assert counter["n"] == 2
