import importlib
import os

import infra.canary_router as canary_router


def test_route_model_canary(monkeypatch):
    monkeypatch.setenv("CANARY_RATE", "1.0")
    importlib.reload(canary_router)
    assert canary_router.route_model().endswith("canary")


def test_route_model_prod(monkeypatch):
    monkeypatch.setenv("CANARY_RATE", "0.0")
    importlib.reload(canary_router)
    assert canary_router.route_model().endswith("production")
