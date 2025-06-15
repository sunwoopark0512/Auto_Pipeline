class OpsLog:
    """Simple operational log model."""

    def __init__(self, module: str, env: str, version: str):
        self.module = module
        self.env = env
        self.version = version

    def record(self):
        """Log to stdout in this mock implementation."""
        print(f"[LOG] {self.module} {self.env} {self.version}")
