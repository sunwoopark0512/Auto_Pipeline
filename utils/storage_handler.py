"""Storage helper supporting local backup when cloud upload fails."""
from __future__ import annotations

import os
import uuid
from typing import Any, Optional

import boto3
from botocore.exceptions import BotoCoreError, ClientError


class StorageHandler:
    def __init__(self, bucket: str, backup_dir: str = "backup") -> None:
        self.bucket = bucket
        self.backup_dir = backup_dir
        os.makedirs(backup_dir, exist_ok=True)
        self.client = boto3.client("s3")

    def _unique_key(self, prefix: str) -> str:
        return f"{prefix}/{uuid.uuid4()}"

    def upload(self, prefix: str, data: bytes) -> str:
        key = self._unique_key(prefix)
        try:
            self.client.put_object(Bucket=self.bucket, Key=key, Body=data)
        except (BotoCoreError, ClientError):  # pragma: no cover - network failure
            path = os.path.join(self.backup_dir, key.replace("/", "_"))
            with open(path, "wb") as f:
                f.write(data)
            return path
        return key
