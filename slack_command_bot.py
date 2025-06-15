from __future__ import annotations

from commands import vinfo


def handle_command(form_data: dict) -> dict:
    """Dispatch incoming Slack command to appropriate handler."""
    command = form_data.get("command")
    if command == "/vinfo":
        return vinfo.run(form_data)
    return {"text": "Unknown command"}
