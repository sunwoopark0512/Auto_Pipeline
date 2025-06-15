import importlib
import sys
import pytest

from utils import env_validator
from utils.env_validator import MissingEnvironmentVariableError


def test_require_env_vars_missing(monkeypatch):
    monkeypatch.delenv('SOME_TOKEN', raising=False)
    with pytest.raises(MissingEnvironmentVariableError):
        env_validator.require_env_vars(['SOME_TOKEN'])


def test_require_env_vars_present(monkeypatch):
    monkeypatch.setenv('SOME_TOKEN', 'abc')
    # Should not raise
    env_validator.require_env_vars(['SOME_TOKEN'])


def test_hook_generator_import_without_token(monkeypatch):
    monkeypatch.delenv('OPENAI_API_KEY', raising=False)
    dummy_module = type(sys)('dotenv')
    dummy_module.load_dotenv = lambda *args, **kwargs: None
    monkeypatch.setitem(sys.modules, 'dotenv', dummy_module)
    monkeypatch.setitem(sys.modules, 'openai', type(sys)('openai'))
    with pytest.raises(MissingEnvironmentVariableError):
        if 'hook_generator' in sys.modules:
            del sys.modules['hook_generator']
        import hook_generator
        importlib.reload(hook_generator)
