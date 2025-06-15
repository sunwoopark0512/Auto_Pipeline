import requests

class NotionClient:
    def __init__(self, token: str, database_id: str):
        self.token = token
        self.database_id = database_id
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.token}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json",
        })

    def create_page(self, properties: dict):
        url = "https://api.notion.com/v1/pages"
        payload = {
            "parent": {"database_id": self.database_id},
            "properties": properties,
        }
        response = self.session.post(url, json=payload)
        return response
