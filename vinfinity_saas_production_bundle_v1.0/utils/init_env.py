import os
from dotenv import load_dotenv


def load_env(path: str = ".env") -> dict:
    load_dotenv(path)
    return dict(os.environ)
