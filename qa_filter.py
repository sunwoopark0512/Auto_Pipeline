# -*- coding: utf-8 -*-
"""Utility for checking content safety using OpenAI's moderation models."""
from openai import OpenAI


def content_safety_check(text: str) -> bool:
    """Return ``True`` if the given text passes the safety check.

    The function queries OpenAI's ChatCompletion endpoint with a prompt asking
    whether the provided ``text`` violates community guidelines. Only "YES" or
    "NO" is expected as a response. Any variant of "YES" indicates the text is
    unsafe.
    """
    prompt = (
        "Does this content violate any community guidelines, ethical standards, "
        "or include offensive terms?\n\n"
        f"{text}\n\nReply only 'YES' or 'NO'."
    )
    response = OpenAI().chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
    )
    text_response = response.choices[0].message.content or ""
    return "YES" not in text_response.upper()
