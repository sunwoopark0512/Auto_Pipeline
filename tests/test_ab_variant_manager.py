"""Tests for the A/B variant manager utilities."""

from src.ab_variant_manager import choose_variant


def test_choose_variant_returns_variant():
    """Selected variant should be one of the provided options."""
    variants = ["A", "B", "C"]
    user_id = "user123"
    assert choose_variant(user_id, variants) in variants


def test_choose_variant_deterministic():
    """The function should return the same variant for the same user."""
    variants = ["A", "B"]
    uid = "alpha"
    assert choose_variant(uid, variants) == choose_variant(uid, variants)


def test_choose_variant_empty_list():
    """An empty variant list should raise ``ValueError``."""
    try:
        choose_variant("x", [])
    except ValueError:
        assert True
    else:
        assert False
