import os, sys
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from unittest.mock import patch
import recursive_kernel.self_audit as self_audit
import recursive_kernel.meta_synthesizer as meta_synthesizer
import recursive_kernel.memory_evolver as memory_evolver
import recursive_kernel.fork_handler as fork_handler


class DummyResp:
    def __init__(self, content):
        self.choices = [type('obj', (), {'message': {'content': content}})]


def dummy_create(*args, **kwargs):
    return DummyResp("ok")


def test_audit_kernel_calls_openai():
    with patch('openai.ChatCompletion.create', side_effect=dummy_create) as mock:
        result = self_audit.audit_kernel('code')
        assert result == 'ok'
        assert mock.called


def test_synthesize_new_kernel():
    with patch('openai.ChatCompletion.create', side_effect=dummy_create) as mock:
        result = meta_synthesizer.synthesize_new_kernel('feedback')
        assert result == 'ok'
        assert mock.called


def test_evolve_from_memory():
    with patch('openai.ChatCompletion.create', side_effect=dummy_create) as mock:
        result = memory_evolver.evolve_from_memory('logs')
        assert result == 'ok'
        assert mock.called


def test_fork_new_entity():
    with patch('openai.ChatCompletion.create', side_effect=dummy_create) as mock:
        result = fork_handler.fork_new_entity('purpose')
        assert result == 'ok'
        assert mock.called
