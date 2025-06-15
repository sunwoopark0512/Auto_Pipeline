import unittest
from unittest import mock
from notion_client import NotionClient


class TestNotionClient(unittest.TestCase):
    @mock.patch("notion_client.requests.post")
    def test_create_page(self, mock_post):
        mock_response = mock.Mock(status_code=200)
        mock_post.return_value = mock_response

        client = NotionClient("token", "db")
        res = client.create_page({"key": "value"})

        mock_post.assert_called_once()
        self.assertIs(res, mock_response)


if __name__ == "__main__":
    unittest.main()
