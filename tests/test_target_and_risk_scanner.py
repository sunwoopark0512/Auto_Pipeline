from unittest.mock import MagicMock

import pytest

from pe_kernel import target_scanner, risk_scanner


def _setup_mock(monkeypatch):
    mock_client = MagicMock()
    mock_choice = MagicMock()
    mock_choice.message.content = "ok"
    mock_client.chat.completions.create.return_value.choices = [mock_choice]
    monkeypatch.setattr(target_scanner.openai, "OpenAI", MagicMock(return_value=mock_client))
    monkeypatch.setattr(risk_scanner.openai, "OpenAI", MagicMock(return_value=mock_client))


@pytest.mark.usefixtures("monkeypatch")
def test_scan_targets(monkeypatch):
    _setup_mock(monkeypatch)
    assert target_scanner.scan_targets("crm") == "ok"


@pytest.mark.usefixtures("monkeypatch")
def test_scan_risks(monkeypatch):
    _setup_mock(monkeypatch)
    assert risk_scanner.scan_risks("crm.com", "python", "smb") == "ok"
