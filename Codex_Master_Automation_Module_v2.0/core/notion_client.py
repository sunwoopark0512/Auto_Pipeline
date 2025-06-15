class NotionClient:
    """Simplified Notion client placeholder used for v2.0 demos."""

    def __init__(self, secret: str, database_id: str):
        self.secret = secret
        self.database_id = database_id

    def create_page(self, payload: dict):
        """Pretend to send a page creation request."""
        print(f"Creating Notion page in {self.database_id} with {payload}")
