import os
from typing import List


def require_vars(vars_: List[str]) -> None:
    missing = [v for v in vars_ if not os.getenv(v)]
    if missing:
        raise EnvironmentError(f"필수 환경 변수 누락: {', '.join(missing)}")
