import sys
from types import SimpleNamespace

sys.path.insert(0, str(__file__).split('/tests')[0])

import pandas as pd

from ceo_kernel import (
    market_scanner,
    competitor_analyzer,
    investor_deck_writer,
    pricing_optimizer,
    saas_cloner,
    cashflow_planner,
)


class DummyClient:
    def __init__(self, text: str):
        self.text = text
        self.chat = SimpleNamespace(completions=SimpleNamespace(create=self._create))

    def _create(self, *args, **kwargs):
        return SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content=self.text))])


def test_market_scanner(monkeypatch):
    monkeypatch.setattr(market_scanner, "client", DummyClient("opportunities"))
    assert market_scanner.scan_market("niche") == "opportunities"


def test_competitor_analyzer(monkeypatch):
    monkeypatch.setattr(competitor_analyzer, "client", DummyClient("summary"))
    assert competitor_analyzer.analyze_competitor("name") == "summary"


def test_investor_deck_writer(monkeypatch):
    monkeypatch.setattr(investor_deck_writer, "client", DummyClient("pitch"))
    assert investor_deck_writer.draft_pitch("saas", "metrics") == "pitch"


def test_pricing_optimizer(capsys):
    pricing_optimizer.optimize_pricing(100, 0.1, 10, 20)
    captured = capsys.readouterr()
    assert "Recommended ARPU" in captured.out


def test_saas_cloner(capsys):
    saas_cloner.clone_saas("http://example.com")
    captured = capsys.readouterr()
    assert "Launching SaaS" in captured.out


def test_cashflow_planner():
    df = cashflow_planner.forecast(1000, 0.1, 0.05, 500)
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
