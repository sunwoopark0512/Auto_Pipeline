"""Base classes for publishing adapters."""
import os
from abc import ABC, abstractmethod

DRYRUN = os.getenv("DRYRUN", "false").lower() == "true"

class PublisherAdapter(ABC):
    """Base interface for publisher adapters."""

    @abstractmethod
    def _real_publish(self, content: dict) -> str:
        """Perform the real publish action and return a URL."""
        raise NotImplementedError

    def publish(self, content: dict) -> str:
        """Publish content if not in DRYRUN mode."""
        if DRYRUN:
            print(f"🔄 DRYRUN – {self.__class__.__name__} skip upload")
            return "DRYRUN_URL"
        return self._real_publish(content)
