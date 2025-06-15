import os
import importlib
from unittest.mock import Mock

import pytest

import notion_dashboard as nd


@pytest.fixture(autouse=True)
def reload_module(monkeypatch):
    monkeypatch.setenv("NOTION_API_KEY", "token")
    monkeypatch.setenv("NOTION_DATABASE_ID", "dbid")
    importlib.reload(nd)
    yield
    importlib.reload(nd)


def test_fetch_notion_data(monkeypatch):
    mock_resp = Mock(status_code=200)
    mock_resp.json.return_value = {"results": ["entry"]}
    monkeypatch.setattr(nd.requests, "post", Mock(return_value=mock_resp))

    result = nd.fetch_notion_data()
    assert result == ["entry"]


def test_generate_performance_chart(tmp_path):
    data = [
        {
            "properties": {
                "Title": {"title": [{"text": {"content": "Title"}}]},
                "Views": {"number": 5}
            }
        }
    ]
    chart = nd.generate_performance_chart(data)
    assert os.path.exists(chart)
    os.remove(chart)


def test_update_notion_dashboard(monkeypatch, tmp_path):
    chart = tmp_path / "chart.png"
    chart.write_text("img")
    monkeypatch.setattr(nd.requests, "post", Mock(return_value=Mock(status_code=200)))
    nd.update_notion_dashboard(str(chart))
    nd.requests.post.assert_called()
