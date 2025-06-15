"""Utility functions for codex package."""

from typing import Any, Dict, Optional


def validate_config(config: Dict[str, Any], required_keys: Optional[list[str]] = None) -> bool:
    """Validate configuration dictionary.

    Args:
        config: Configuration dictionary to validate
        required_keys: List of required keys

    Returns:
        True if configuration is valid, False otherwise
    """
    if required_keys is None:
        return True

    return all(key in config for key in required_keys)


def get_config_value(
    config: Dict[str, Any],
    key: str,
    default: Any = None,
    value_type: Optional[type] = None
) -> Any:
    """Get value from configuration with optional type checking.

    Args:
        config: Configuration dictionary
        key: Key to look up
        default: Default value if key not found
        value_type: Expected type of value

    Returns:
        Value from config or default
    """
    value = config.get(key, default)
    if value_type is not None and value is not None:
        if not isinstance(value, value_type):
            raise TypeError(f"Config value for {key} must be of type {value_type.__name__}")
    return value
