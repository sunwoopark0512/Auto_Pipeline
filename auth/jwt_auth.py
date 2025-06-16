import os
import json
import time
import hmac
import hashlib
import base64
from typing import Optional

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "changeme")


def _b64encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def _b64decode(data: str) -> bytes:
    padding = '=' * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


def generate_token(user_id: str, expires_in: int = 3600) -> str:
    """Generate a simple JWT token with HS256 signing."""
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {"user_id": user_id, "exp": int(time.time()) + expires_in}

    header_b64 = _b64encode(json.dumps(header).encode())
    payload_b64 = _b64encode(json.dumps(payload).encode())
    signing_input = f"{header_b64}.{payload_b64}".encode()
    signature = hmac.new(JWT_SECRET_KEY.encode(), signing_input, hashlib.sha256).digest()
    signature_b64 = _b64encode(signature)
    return f"{header_b64}.{payload_b64}.{signature_b64}"


def validate_token(token: str) -> Optional[str]:
    """Validate the token and return the user_id if valid."""
    try:
        header_b64, payload_b64, signature_b64 = token.split('.')
    except ValueError:
        return None

    signing_input = f"{header_b64}.{payload_b64}".encode()
    expected_sig = hmac.new(JWT_SECRET_KEY.encode(), signing_input, hashlib.sha256).digest()
    try:
        provided_sig = _b64decode(signature_b64)
    except (TypeError, ValueError):
        return None

    if not hmac.compare_digest(expected_sig, provided_sig):
        return None

    try:
        payload_data = json.loads(_b64decode(payload_b64).decode())
    except (json.JSONDecodeError, ValueError):
        return None

    if payload_data.get('exp') and time.time() > payload_data['exp']:
        return None

    return payload_data.get('user_id')
