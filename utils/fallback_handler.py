"""Fallback helpers for LLM failures."""
from __future__ import annotations

from typing import Optional


def fallback_message() -> str:
    return "[자동 응답 실패: 후처리 필요]"


def safe_llm_call(prompt: str) -> str:
    from .llm_client import call_llm

    response = call_llm(prompt)
    if response is None:
        return fallback_message()
    return response
