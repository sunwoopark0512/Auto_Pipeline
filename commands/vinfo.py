from __future__ import annotations

def run(form_data: dict) -> dict:
    """Return a greeting for Slack."""
    user_name = form_data.get("user_name", "unknown")
    text = f":robot_face: Hello, {user_name}!"
    return {"text": text}
