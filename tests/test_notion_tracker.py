from unittest import mock

import notion_tracker


def test_create_notion_page_success():
    with mock.patch('requests.post') as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.text = 'ok'
        assert notion_tracker.create_notion_page('title', 'Published', 'WP', '2024-01-01', 10)
        mock_post.assert_called_once()


def test_create_notion_page_failure():
    with mock.patch('requests.post') as mock_post:
        mock_post.return_value.status_code = 400
        mock_post.return_value.text = 'error'
        assert not notion_tracker.create_notion_page('title', 'Published', 'WP', '2024-01-01', 10)


def test_update_notion_page_success():
    with mock.patch('requests.patch') as mock_patch:
        mock_patch.return_value.status_code = 200
        mock_patch.return_value.text = 'ok'
        assert notion_tracker.update_notion_page('pageid', 123)
        mock_patch.assert_called_once()


def test_update_notion_page_failure():
    with mock.patch('requests.patch') as mock_patch:
        mock_patch.return_value.status_code = 404
        mock_patch.return_value.text = 'not found'
        assert not notion_tracker.update_notion_page('pageid', 123)


def test_track_performance():
    data = {
        'title': 'Sample',
        'status': 'Published',
        'platform': 'WP',
        'post_date': '2024-01-01',
        'views': 50,
    }
    with mock.patch('notion_tracker.create_notion_page') as mock_create:
        mock_create.return_value = True
        assert notion_tracker.track_performance(data)
        mock_create.assert_called_once()
