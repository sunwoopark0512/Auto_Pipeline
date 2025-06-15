"""A/B variant selection utilities."""

from hashlib import sha256
from typing import Iterable, Sequence


def choose_variant(user_id: str, variants: Sequence[str]) -> str:
    """Deterministically choose a variant based on ``user_id``.

    Parameters
    ----------
    user_id:
        Identifier used to select the variant.
    variants:
        Non-empty sequence of variant names.

    Returns
    -------
    str
        Selected variant from ``variants``.

    Raises
    ------
    ValueError
        If ``variants`` is empty.
    """
    if not variants:
        raise ValueError("variants sequence cannot be empty")
    index = int(sha256(user_id.encode()).hexdigest(), 16) % len(variants)
    return variants[index]
