import os, sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from unittest import mock

import rag.prompt_compressor as pc


def test_compress_context_calls_model(monkeypatch):
    fake_tokenizer = mock.MagicMock()
    fake_model = mock.MagicMock()
    fake_model.generate.return_value = [[1, 2, 3]]
    fake_tokenizer.decode.return_value = "compressed"
    monkeypatch.setattr(pc, "_load", lambda: (fake_model, fake_tokenizer))
    result = pc.compress_context("some text")
    assert result == "compressed"
    fake_model.generate.assert_called_once()
