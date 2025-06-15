import os
from typing import Iterable

class MissingEnvironmentVariableError(EnvironmentError):
    """Raised when required environment variables are missing."""


def require_env_vars(vars: Iterable[str]) -> None:
    """Ensure required environment variables are present.

    Args:
        vars: Iterable of environment variable names to validate.

    Raises:
        MissingEnvironmentVariableError: if any variable is missing.
    """
    missing = [var for var in vars if not os.getenv(var)]
    if missing:
        raise MissingEnvironmentVariableError(
            "Missing required environment variables: " + ", ".join(missing)
        )
