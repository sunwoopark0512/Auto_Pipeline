"""Core module for codex package."""

from typing import Any, Dict, Optional


class CodexModule:
    """Base class for all codex modules."""

    def __init__(self, name: str, config: Optional[Dict[str, Any]] = None) -> None:
        """Initialize the module.

        Args:
            name: Module name
            config: Optional configuration dictionary
        """
        self.name = name
        self.config = config or {}
        self._initialized = False

    def initialize(self) -> None:
        """Initialize the module."""
        if not self._initialized:
            self._setup()
            self._initialized = True

    def _setup(self) -> None:
        """Internal setup method."""
        pass  # Placeholder for actual implementation

    def get_status(self) -> Dict[str, Any]:
        """Get module status.

        Returns:
            Dict containing module status information
        """
        return {
            "name": self.name,
            "initialized": self._initialized,
            "config": self.config
        }
