from unittest.mock import MagicMock, patch
import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from modules.keyword_generator import generate_keywords
from modules.content_writer import generate_article
from modules.editor_seo_optimizer import optimize_text
from modules.qa_filter import content_safety_check
from modules.hook_uploader import upload_to_wordpress
from modules.slack_notifier import send_slack_message
from modules.notion_sync import update_notion_status
from auth_utils import get_user_profile
from billing_utils import check_user_quota


@patch('modules.keyword_generator.OpenAI')
def test_generate_keywords(mock_openai):
    mock_client = MagicMock()
    mock_openai.return_value = mock_client
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content='kw1\nkw2'))]
    mock_client.chat.completions.create.return_value = mock_response
    result = generate_keywords('topic')
    assert result == ['kw1', 'kw2']


@patch('modules.content_writer.OpenAI')
def test_generate_article(mock_openai):
    mock_client = MagicMock()
    mock_openai.return_value = mock_client
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content='article'))]
    mock_client.chat.completions.create.return_value = mock_response
    result = generate_article('keyword')
    assert result == 'article'


@patch('modules.editor_seo_optimizer.OpenAI')
def test_optimize_text(mock_openai):
    mock_client = MagicMock()
    mock_openai.return_value = mock_client
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content='optimized'))]
    mock_client.chat.completions.create.return_value = mock_response
    result = optimize_text('text')
    assert result == 'optimized'


@patch('modules.qa_filter.OpenAI')
def test_content_safety_check(mock_openai):
    mock_client = MagicMock()
    mock_openai.return_value = mock_client
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content='NO'))]
    mock_client.chat.completions.create.return_value = mock_response
    assert content_safety_check('text')


@patch('modules.hook_uploader.requests.post')
def test_upload_to_wordpress(mock_post):
    mock_resp = MagicMock(status_code=201)
    mock_resp.json.return_value = {'id': 1}
    mock_post.return_value = mock_resp
    status, data = upload_to_wordpress('title', 'content', 'slug', 'token')
    assert status == 201
    assert data == {'id': 1}


@patch('modules.slack_notifier.requests.post')
def test_send_slack_message(mock_post):
    mock_resp = MagicMock(status_code=200)
    mock_post.return_value = mock_resp
    status = send_slack_message('http://example.com', 'hi')
    assert status == 200


@patch('modules.notion_sync.Client')
def test_update_notion_status(mock_client):
    instance = mock_client.return_value
    update_notion_status('token', 'page', 'Done')
    instance.pages.update.assert_called_once()


@patch('auth_utils.psycopg2.connect')
def test_get_user_profile(mock_connect):
    conn = mock_connect.return_value
    cursor = conn.cursor.return_value
    cursor.fetchone.return_value = ('pro', 'key')
    result = get_user_profile(1)
    assert result == ('pro', 'key')
    cursor.execute.assert_called_once()


@patch('billing_utils.get_user_profile')
@patch('billing_utils.get_content_count')
def test_check_user_quota(mock_count, mock_profile):
    mock_profile.return_value = ('free', 'key')
    mock_count.return_value = 0
    check_user_quota(1)
    mock_count.return_value = 10
    with pytest.raises(Exception):
        check_user_quota(1)
