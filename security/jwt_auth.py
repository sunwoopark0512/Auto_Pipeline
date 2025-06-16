"""JWT utility functions for creating and validating tokens.

The signing secret is expected to be provided via the ``JWT_SECRET_KEY``
environment variable. Example usage::

    from security.jwt_auth import SECRET, generate_token, validate_token

    token = generate_token("user123", secret=SECRET)
    claims = validate_token(token, SECRET)
    print(claims["sub"])  # "user123"
"""

from __future__ import annotations

import os
from datetime import datetime, timedelta
from typing import Dict, Any

import jwt


class TokenValidationError(Exception):
    """Raised when a JWT is invalid or expired."""


def generate_token(user_id: str, *, secret: str, expiry_hours: int = 1) -> str:
    """Return a signed JWT for ``user_id``.

    Parameters
    ----------
    user_id: str
        Identifier of the user.
    secret: str
        Signing secret key.
    expiry_hours: int, optional
        Hours until the token expires. Defaults to ``1``.
    """
    payload = {
        "sub": user_id,
        "exp": datetime.utcnow() + timedelta(hours=expiry_hours),
    }
    return jwt.encode(payload, secret, algorithm="HS256")


def validate_token(token: str, secret: str) -> Dict[str, Any]:
    """Validate ``token`` using ``secret`` and return its payload.

    Raises ``TokenValidationError`` if the token is invalid or expired.
    """
    try:
        return jwt.decode(token, secret, algorithms=["HS256"])
    except jwt.ExpiredSignatureError as exc:
        raise TokenValidationError("Token has expired") from exc
    except jwt.InvalidTokenError as exc:
        raise TokenValidationError("Invalid token") from exc


SECRET = os.getenv("JWT_SECRET_KEY")
