"""Check if PyPI egress is allowed."""

import socket

try:
    socket.create_connection(("pypi.org", 443), timeout=3)
    print("✅ PyPI access OK")
except Exception:
    print("❌ PyPI access blocked. Check firewall or cloud egress rules.")
