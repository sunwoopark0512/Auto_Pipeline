"""Security utilities for Auto_Pipeline.

This module provides basic implementations of common security features
such as JWT-based authentication, AES encryption, simple API key
verification and role based access control. These utilities are meant to
be used by other scripts when security is required.
"""

from __future__ import annotations

import os
from datetime import datetime, timedelta
from typing import Dict, Optional, Any

import jwt  # PyJWT
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


class AuthSystem:
    """Simple JWT authentication helper."""

    def __init__(self, secret_key: str, expiry_hours: int = 1) -> None:
        self.secret_key = secret_key
        self.expiry_hours = expiry_hours

    def generate_token(self, user_id: str | int) -> str:
        """Generate a JWT token for ``user_id``."""
        expiration = datetime.utcnow() + timedelta(hours=self.expiry_hours)
        payload = {"user_id": user_id, "exp": expiration}
        token = jwt.encode(payload, self.secret_key, algorithm="HS256")
        # PyJWT>=2 returns str by default
        return token

    def validate_token(self, token: str) -> Dict[str, Any] | str:
        """Validate ``token`` and return payload or error message."""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            return "Token expired"
        except jwt.InvalidTokenError:
            return "Invalid token"


class DataEncryption:
    """AES-256 CBC encryption helper."""

    def __init__(self, key: Optional[bytes] = None, iv: Optional[bytes] = None) -> None:
        self.key = key or os.urandom(32)
        self.iv = iv or os.urandom(16)

    def _cipher(self) -> Cipher:
        return Cipher(algorithms.AES(self.key), modes.CBC(self.iv), backend=default_backend())

    def encrypt_data(self, data: bytes) -> bytes:
        cipher = self._cipher()
        encryptor = cipher.encryptor()
        padding_len = 16 - (len(data) % 16)
        padded = data + bytes([padding_len]) * padding_len
        return encryptor.update(padded) + encryptor.finalize()

    def decrypt_data(self, encrypted_data: bytes) -> bytes:
        cipher = self._cipher()
        decryptor = cipher.decryptor()
        padded = decryptor.update(encrypted_data) + decryptor.finalize()
        padding_len = padded[-1]
        return padded[:-padding_len]


class APIKeyAuth:
    """Simple API key verification."""

    def __init__(self, valid_key: str) -> None:
        self.valid_key = valid_key

    def verify(self, provided_key: Optional[str]) -> bool:
        return provided_key == self.valid_key


class UserRole:
    """Role-based permission helper."""

    def __init__(self, role: str) -> None:
        self.role = role
        self.permissions = self._set_permissions(role)

    @staticmethod
    def _set_permissions(role: str) -> list[str]:
        if role == "admin":
            return ["read", "write", "delete"]
        if role == "editor":
            return ["read", "write"]
        return ["read"]

    def has_permission(self, action: str) -> bool:
        return action in self.permissions


class IntrusionDetection:
    """Very small IP whitelist checker."""

    def __init__(self, allowed_ips: list[str]) -> None:
        self.allowed_ips = allowed_ips

    def check_ip(self, ip: str) -> str:
        if ip not in self.allowed_ips:
            return f"Intrusion detected from IP: {ip}"
        return "Access granted"


__all__ = [
    "AuthSystem",
    "DataEncryption",
    "APIKeyAuth",
    "UserRole",
    "IntrusionDetection",
]

