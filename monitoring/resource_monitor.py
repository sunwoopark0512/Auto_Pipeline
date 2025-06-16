import os
import threading
import time
from datetime import datetime

import psutil


class ResourceMonitor:
    """Background monitor that logs CPU and memory usage."""

    def __init__(self, interval: float = 1.0, log_file: str = "logs/resource_monitor.log"):
        self.interval = interval
        self.log_file = log_file
        self._thread = None
        self._stop_event = threading.Event()

    def _ensure_log_dir(self):
        directory = os.path.dirname(self.log_file)
        if directory:
            os.makedirs(directory, exist_ok=True)

    def _monitor(self):
        self._ensure_log_dir()
        with open(self.log_file, "a") as f:
            while not self._stop_event.is_set():
                cpu = psutil.cpu_percent(interval=None)
                mem = psutil.virtual_memory().percent
                timestamp = datetime.now().isoformat()
                f.write(f"{timestamp}, cpu={cpu}, mem={mem}\n")
                f.flush()
                time.sleep(self.interval)

    def start(self):
        if self._thread and self._thread.is_alive():
            return
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._monitor, daemon=True)
        self._thread.start()

    def stop(self):
        self._stop_event.set()
        if self._thread:
            self._thread.join()


_default_monitor = ResourceMonitor()


def start_monitoring():
    """Start the default resource monitor."""
    _default_monitor.start()


def stop_monitoring():
    """Stop the default resource monitor."""
    _default_monitor.stop()
