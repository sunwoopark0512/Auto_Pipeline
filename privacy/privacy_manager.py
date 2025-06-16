import argparse
import json
import logging
import os


class PrivacyManager:
    """Utility class to manage user data in local storage."""

    def __init__(self, storage_path: str = "data/user_data.json") -> None:
        self.storage_path = storage_path

    def request_data_deletion(self, user_id: str) -> bool:
        """Remove records for ``user_id`` from the local storage file."""
        if not os.path.exists(self.storage_path):
            logging.warning("Storage file not found: %s", self.storage_path)
            return False

        try:
            with open(self.storage_path, "r", encoding="utf-8") as f:
                records = json.load(f)
        except json.JSONDecodeError:
            logging.error("Invalid JSON in %s", self.storage_path)
            return False

        original_len = len(records)
        records = [r for r in records if r.get("user_id") != user_id]

        if len(records) == original_len:
            logging.info("No records found for user %s", user_id)
        else:
            with open(self.storage_path, "w", encoding="utf-8") as f:
                json.dump(records, f, ensure_ascii=False, indent=2)
            logging.info("Deleted data for user %s", user_id)
        return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manage privacy operations")
    parser.add_argument("--delete", metavar="USER_ID", help="Delete a user's data")
    args = parser.parse_args()

    if args.delete:
        manager = PrivacyManager()
        success = manager.request_data_deletion(args.delete)
        if success:
            print(f"User {args.delete} data deleted.")
        else:
            print(f"No data deleted for user {args.delete}.")

