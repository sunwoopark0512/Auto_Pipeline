import unittest
from unittest.mock import MagicMock, patch

import delete_notion_page as dnp

class TestDeleteNotionPage(unittest.TestCase):
    @patch('delete_notion_page.notion')
    def test_find_page_id_by_keyword(self, mock_notion):
        mock_notion.databases.query.return_value = {'results': [{'id': '123'}]}
        page_id = dnp.find_page_id_by_keyword('테스트')
        self.assertEqual(page_id, '123')
        mock_notion.databases.query.assert_called_once()

    @patch('delete_notion_page.notion')
    def test_delete_page(self, mock_notion):
        result = dnp.delete_page('abc')
        self.assertTrue(result)
        mock_notion.pages.update.assert_called_once_with('abc', archived=True)

    @patch('delete_notion_page.find_page_id_by_keyword', return_value='pid')
    @patch('delete_notion_page.delete_page', return_value=True)
    def test_delete_by_keyword(self, mock_delete, mock_find):
        res = dnp.delete_by_keyword('kw')
        self.assertTrue(res)
        mock_find.assert_called_once_with('kw')
        mock_delete.assert_called_once_with('pid')

if __name__ == '__main__':
    unittest.main()
