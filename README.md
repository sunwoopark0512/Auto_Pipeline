# Auto Pipeline

Utility scripts for generating marketing hooks and uploading them to Notion.

## JWT Authentication

Some future services may expose endpoints that require token-based authentication. The `auth/jwt_auth.py` module provides very small helper functions to issue and verify JSON Web Tokens without external dependencies.

Set `JWT_SECRET_KEY` in your environment and use as follows:

```python
from auth.jwt_auth import generate_token, validate_token

# create a token for a user id
token = generate_token("user123")

# later validate it
user_id = validate_token(token)
if user_id:
    print("valid for", user_id)
```

Tokens expire in one hour by default. Adjust the expiration with the `expires_in` parameter when calling `generate_token`.
