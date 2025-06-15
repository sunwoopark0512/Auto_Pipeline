from unittest import mock
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import publish_automation as pa


def _mock_response(status_code: int, text: str = ""):
    resp = mock.Mock()
    resp.status_code = status_code
    resp.text = text
    return resp


@mock.patch("publish_automation.requests.post")
def test_publish_to_wordpress_success(mock_post):
    mock_post.return_value = _mock_response(201)
    assert pa.publish_to_wordpress("title", "content") is True
    mock_post.assert_called_once()


@mock.patch("publish_automation.requests.post")
def test_publish_to_wordpress_failure(mock_post):
    mock_post.return_value = _mock_response(400, "err")
    assert pa.publish_to_wordpress("title", "content") is False


@mock.patch("publish_automation.requests.post")
def test_publish_to_twitter_success(mock_post):
    mock_post.return_value = _mock_response(201)
    assert pa.publish_to_twitter("hi") is True


@mock.patch("publish_automation.requests.post")
def test_publish_to_twitter_failure(mock_post):
    mock_post.return_value = _mock_response(500, "err")
    assert pa.publish_to_twitter("hi") is False


@mock.patch("publish_automation.requests.post")
def test_publish_to_youtube_success(mock_post):
    mock_post.return_value = _mock_response(200)
    assert pa.publish_to_youtube("id", "title", "desc") is True


@mock.patch("publish_automation.requests.post")
def test_publish_to_youtube_failure(mock_post):
    mock_post.return_value = _mock_response(403, "err")
    assert pa.publish_to_youtube("id", "title", "desc") is False


def test_publish_to_rss():
    assert pa.publish_to_rss("title", "content", "http://example.com/feed") is True


def test_send_newsletter():
    assert pa.send_newsletter("subject", "content", ["a@example.com"]) is True


@mock.patch("publish_automation.publish_to_wordpress")
def test_automate_publish_dispatch(mock_wp):
    mock_wp.return_value = True
    assert pa.automate_publish("c", "t", platform="wordpress") is True
    mock_wp.assert_called_once()

