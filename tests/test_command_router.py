import os, sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from command_router import handle_command


class DummyForm(dict):
    def get(self, key, default=None):
        return super().get(key, default)


def test_handle_known_commands():
    form = DummyForm(user_name="tester")
    resp = handle_command("/vinfo", form)
    assert "안녕하세요" in resp["text"]

    resp = handle_command("/vstart", form)
    assert "파이프라인" in resp["text"]

    resp = handle_command("/vcheck", form)
    assert "점검" in resp["text"]


def test_handle_unknown_command():
    resp = handle_command("/unknown", {})
    assert resp["response_type"] == "ephemeral"
