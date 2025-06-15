import os
import ldclient
from ldclient.config import Config

LD_SDK_KEY = os.getenv("LAUNCHDARKLY_SDK_KEY", "")
ldclient.set_config(Config(sdk_key=LD_SDK_KEY))
client = ldclient.get()

def flag_enabled(key: str, user_key: str = "system") -> bool:
    """Return LaunchDarkly flag status for the given key."""
    if client.is_initialized():
        return client.variation(key, {"key": user_key}, False)  # type: ignore[arg-type]
    return False
