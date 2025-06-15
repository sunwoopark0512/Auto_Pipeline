import requests

class NotionClient:
    def __init__(self, notion_token, database_id):
        self.api_url = "https://api.notion.com/v1/pages"
        self.database_id = database_id
        self.headers = {
            "Authorization": f"Bearer {notion_token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }

    def create_page(self, payload):
        response = requests.post(self.api_url, headers=self.headers, json=payload)
        return response
