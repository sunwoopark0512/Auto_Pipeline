"""Tests for utils module."""

import pytest
from codex.utils import validate_config, get_config_value


def test_validate_config_empty():
    """Test config validation with no required keys."""
    assert validate_config({})
    assert validate_config({}, None)
    assert validate_config({"key": "value"})


def test_validate_config_required():
    """Test config validation with required keys."""
    config = {"key1": "value1", "key2": "value2"}
    assert validate_config(config, ["key1"])
    assert validate_config(config, ["key1", "key2"])
    assert not validate_config(config, ["key1", "key3"])


def test_get_config_value():
    """Test get_config_value function."""
    config = {"key": "value", "number": 42}

    assert get_config_value(config, "key") == "value"
    assert get_config_value(config, "missing", "default") == "default"
    assert get_config_value(config, "number", value_type=int) == 42

    with pytest.raises(TypeError):
        get_config_value(config, "key", value_type=int)
