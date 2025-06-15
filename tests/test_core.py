"""Tests for core module."""

from codex.core import CodexModule


def test_module_initialization():
    """Test basic module initialization."""
    module = CodexModule("test")
    assert module.name == "test"
    assert not module._initialized
    assert isinstance(module.config, dict)


def test_module_with_config():
    """Test module with configuration."""
    config = {"key": "value"}
    module = CodexModule("test", config)
    assert module.config == config


def test_initialize():
    """Test module initialization."""
    module = CodexModule("test")
    module.initialize()
    assert module._initialized


def test_get_status():
    """Test get_status method."""
    config = {"key": "value"}
    module = CodexModule("test", config)
    status = module.get_status()

    assert status["name"] == "test"
    assert not status["initialized"]
    assert status["config"] == config
