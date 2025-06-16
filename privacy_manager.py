import os
import json
import logging


def request_data_deletion(user_id: str, storage_path: str) -> int:
    """Remove records associated with ``user_id`` from a JSON file.

    Parameters
    ----------
    user_id : str
        Identifier of the user whose data should be removed.
    storage_path : str
        Path to the JSON file storing the data.

    Returns
    -------
    int
        Number of records removed.
    """
    if not os.path.exists(storage_path):
        logging.info("Storage file not found: %s", storage_path)
        return 0

    try:
        with open(storage_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        logging.warning("Failed reading %s: %s", storage_path, e)
        return 0

    removed = 0
    modified = False

    if isinstance(data, list):
        new_data = []
        for entry in data:
            if isinstance(entry, dict) and (
                entry.get("user_id") == user_id
                or entry.get("user") == user_id
                or entry.get("id") == user_id
            ):
                removed += 1
                modified = True
                logging.info("Removed entry for user %s from %s", user_id, storage_path)
            else:
                new_data.append(entry)
        data = new_data
    elif isinstance(data, dict):
        if user_id in data:
            removed += 1
            modified = True
            data.pop(user_id)
            logging.info("Removed key %s from %s", user_id, storage_path)
        elif "records" in data and isinstance(data["records"], list):
            new_records = []
            for entry in data["records"]:
                if isinstance(entry, dict) and entry.get("user_id") == user_id:
                    removed += 1
                    modified = True
                    logging.info(
                        "Removed record for user %s from %s", user_id, storage_path
                    )
                else:
                    new_records.append(entry)
            data["records"] = new_records
    else:
        logging.warning("Unsupported JSON format in %s", storage_path)
        return 0

    if modified:
        try:
            with open(storage_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logging.error("Failed writing %s: %s", storage_path, e)
            return 0

    return removed

