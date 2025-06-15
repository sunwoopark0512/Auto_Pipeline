import os, sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from unittest import mock

import aiops.cost_guard as cg


def test_gpu_cost_forecast(monkeypatch):
    fake_client = mock.MagicMock()
    fake_client.get_cost_forecast.return_value = {
        "ForecastResultsByTime": [{"MeanValue": "100"}]
    }
    monkeypatch.setattr(cg.boto3, "client", lambda name: fake_client)
    assert cg.gpu_cost_forecast(200) is True
