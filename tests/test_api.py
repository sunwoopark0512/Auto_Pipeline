import os, sys; sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import os
from fastapi.testclient import TestClient
from api.main import app


def test_read_keywords(tmp_path, monkeypatch):
    data_file = tmp_path / "hooks.json"
    data_file.write_text('[{"keyword": "x", "hook_lines": [], "source": "t", "score": 1}]')
    monkeypatch.setattr("api.main.DATA", data_file)
    monkeypatch.setenv("API_KEYS", "abc")
    monkeypatch.setattr("api.main.API_KEYS", {"abc"}, raising=False)
    client = TestClient(app)
    resp = client.get("/v1/keywords?limit=1", headers={"X-API-KEY": "abc"})
    assert resp.status_code == 200
    assert resp.json()["count"] == 1
