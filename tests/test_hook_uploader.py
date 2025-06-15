import os
import sys
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import importlib
import hook_uploader

TEST_HOOK = {
    "keyword": "test keyword",
    "blog_paragraphs": ["p1", "p2"],
    "hook_lines": ["line1"],
    "video_titles": ["title1"]
}

@mock.patch("hook_uploader.requests.post")
def test_post_to_wordpress(mock_post):
    os.environ["WORDPRESS_API_URL"] = "https://wp.example.com"
    os.environ["WORDPRESS_API_TOKEN"] = "token"
    importlib.reload(hook_uploader)
    hook_uploader.post_to_wordpress(TEST_HOOK)
    assert mock_post.called
    url = mock_post.call_args[0][0]
    assert url.endswith("/posts")

@mock.patch("hook_uploader.requests.post")
def test_post_to_medium(mock_post):
    os.environ["MEDIUM_API_URL"] = "https://medium.example.com"
    os.environ["MEDIUM_API_TOKEN"] = "token"
    importlib.reload(hook_uploader)
    hook_uploader.post_to_medium(TEST_HOOK)
    assert mock_post.called
    url = mock_post.call_args[0][0]
    assert url.endswith("/posts")

@mock.patch("hook_uploader.requests.post")
def test_post_to_twitter(mock_post):
    os.environ["TWITTER_API_URL"] = "https://api.twitter.com"
    os.environ["TWITTER_BEARER_TOKEN"] = "token"
    importlib.reload(hook_uploader)
    hook_uploader.post_to_twitter(TEST_HOOK)
    assert mock_post.called
    url = mock_post.call_args[0][0]
    assert url.endswith("/tweets")

@mock.patch("hook_uploader.requests.post")
def test_post_to_youtube(mock_post):
    os.environ["YOUTUBE_API_URL"] = "https://youtube.example.com"
    os.environ["YOUTUBE_API_TOKEN"] = "token"
    importlib.reload(hook_uploader)
    hook_uploader.post_to_youtube(TEST_HOOK)
    assert mock_post.called
    url = mock_post.call_args[0][0]
    assert url.endswith("/videos")
