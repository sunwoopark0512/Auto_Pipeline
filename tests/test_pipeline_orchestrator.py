import unittest
from unittest.mock import patch
import pipeline_orchestrator


class PipelineOrchestratorTests(unittest.TestCase):
    @patch('pipeline_orchestrator.upload_to_wordpress')
    @patch('pipeline_orchestrator.content_safety_check')
    @patch('pipeline_orchestrator.optimize_text')
    @patch('pipeline_orchestrator.generate_article')
    @patch('pipeline_orchestrator.generate_keywords')
    def test_run_pipeline_uploads_when_safe(self, mock_keywords, mock_article, mock_optimize, mock_check, mock_upload):
        mock_keywords.return_value = ['kw']
        mock_article.return_value = 'draft'
        mock_optimize.return_value = 'revised'
        mock_check.return_value = True
        mock_upload.return_value = (200, {})

        pipeline_orchestrator.run_pipeline('topic', 'token')

        mock_keywords.assert_called_once_with('topic')
        mock_article.assert_called_once_with('kw')
        mock_optimize.assert_called_once_with('draft')
        mock_check.assert_called_once_with('revised')
        mock_upload.assert_called_once_with(title='kw', content='revised', slug='kw', token='token')

    @patch('pipeline_orchestrator.upload_to_wordpress')
    @patch('pipeline_orchestrator.content_safety_check')
    @patch('pipeline_orchestrator.optimize_text')
    @patch('pipeline_orchestrator.generate_article')
    @patch('pipeline_orchestrator.generate_keywords')
    def test_run_pipeline_skips_when_unsafe(self, mock_keywords, mock_article, mock_optimize, mock_check, mock_upload):
        mock_keywords.return_value = ['kw']
        mock_article.return_value = 'draft'
        mock_optimize.return_value = 'revised'
        mock_check.return_value = False

        pipeline_orchestrator.run_pipeline('topic', 'token')

        mock_upload.assert_not_called()


if __name__ == '__main__':
    unittest.main()
