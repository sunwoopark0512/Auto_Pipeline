"""LLM client with timeout and retry handling."""
from __future__ import annotations

import logging
from typing import Optional

import openai  # type: ignore


def call_llm(prompt: str, *, timeout: int = 10, retries: int = 3) -> Optional[str]:
    """Call OpenAI chat completion API with retries."""
    for attempt in range(1, retries + 1):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                request_timeout=timeout,
            )
            return response.choices[0].message["content"]
        except Exception as exc:  # pragma: no cover - network error path
            logging.warning("LLM call failed %s/%s: %s", attempt, retries, exc)
    return None
