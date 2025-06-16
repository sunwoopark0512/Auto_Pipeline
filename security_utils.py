"""Security utilities for Auto_Pipeline.

This module provides encryption, JWT authentication, and privacy
management utilities to help protect sensitive data and comply with
privacy regulations such as GDPR and CCPA.
"""

import os
from datetime import datetime, timedelta
from typing import Any, Dict

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import jwt


class EncryptionUtil:
    """Utility for AES-256-CBC encryption and decryption."""

    def __init__(self, key: bytes | None = None, iv: bytes | None = None) -> None:
        self.key = key or os.urandom(32)
        self.iv = iv or os.urandom(16)

    def encrypt(self, data: bytes) -> bytes:
        """Encrypt data using AES-256-CBC."""
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(self.iv), backend=default_backend())
        encryptor = cipher.encryptor()
        padding = 16 - len(data) % 16
        padded = data + bytes([padding]) * padding
        return encryptor.update(padded) + encryptor.finalize()

    def decrypt(self, encrypted_data: bytes) -> bytes:
        """Decrypt AES-256-CBC encrypted data."""
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(self.iv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted = decryptor.update(encrypted_data) + decryptor.finalize()
        padding = decrypted[-1]
        return decrypted[:-padding]


class JWTAuthentication:
    """Simple JWT authentication helper."""

    def __init__(self, secret_key: str) -> None:
        self.secret_key = secret_key

    def generate_token(self, user_id: Any, expires_hours: int = 1) -> str:
        """Generate a JWT token for the given user ID."""
        exp = datetime.utcnow() + timedelta(hours=expires_hours)
        payload = {"user_id": user_id, "exp": exp}
        return jwt.encode(payload, self.secret_key, algorithm="HS256")

    def validate_token(self, token: str) -> Dict[str, Any] | str:
        """Validate a JWT token and return the payload."""
        try:
            return jwt.decode(token, self.secret_key, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return "Token expired"
        except jwt.InvalidTokenError:
            return "Invalid token"


class PrivacyManager:
    """Handle GDPR/CCPA data deletion requests."""

    def __init__(self, database: Dict[str, Any]):
        self.database = database

    def request_data_deletion(self, user_id: str) -> str:
        if user_id in self.database:
            del self.database[user_id]
            return f"User {user_id}'s data has been deleted."
        return "User data not found."
