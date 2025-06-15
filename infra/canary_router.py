"""Canary routing utilities."""
from __future__ import annotations

import random
import os
from typing import Final

CANARY_RATE: Final[float] = float(
    os.getenv("CANARY_RATE", 0.1)
)


def route_model() -> str:
    """Return the model identifier based on canary rate."""
    if random.random() < CANARY_RATE:
        return "gpt-4o-vinfinity-canary"
    return "gpt-4o-production"


if __name__ == "__main__":
    print(route_model())
