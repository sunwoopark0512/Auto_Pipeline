from unittest.mock import patch, call
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src import content_generator


@patch('src.content_generator.update_db_status')
def test_generate_content_success(mock_update):
    result = content_generator.generate_content('AI', 'English')
    assert result['title'] == 'Generated content for AI'
    mock_update.assert_called_with('Content Generation', 'Success')


@patch('src.content_generator.logger')
@patch('src.content_generator.update_db_status')
def test_generate_content_error(mock_update, mock_logger):
    mock_update.side_effect = [Exception('boom'), None]
    result = content_generator.generate_content('AI', 'English')
    assert result is None
    mock_update.assert_has_calls([
        call('Content Generation', 'Success'),
        call('Content Generation', 'Failed', 'boom'),
    ])
    mock_logger.error.assert_called()
