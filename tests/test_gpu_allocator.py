import importlib
from unittest.mock import MagicMock

import sys
import infra.gpu_allocator as gpu_allocator


def mock_client(_: str):
    mock = MagicMock()
    mock.describe_spot_price_history.return_value = {
        "SpotPriceHistory": [{"SpotPrice": "5.0"}]
    }
    return mock


def test_allocate_gpu_spot(monkeypatch):
    monkeypatch.setitem(sys.modules, "boto3", MagicMock(client=mock_client))
    importlib.reload(gpu_allocator)
    assert gpu_allocator.allocate_gpu(price_threshold=6.0) == "spot"


def test_allocate_gpu_on_demand(monkeypatch):
    def client(_: str):
        mock = MagicMock()
        mock.describe_spot_price_history.return_value = {
            "SpotPriceHistory": [{"SpotPrice": "7.0"}]
        }
        return mock

    monkeypatch.setitem(sys.modules, "boto3", MagicMock(client=client))
    importlib.reload(gpu_allocator)
    assert gpu_allocator.allocate_gpu(price_threshold=6.0) == "on-demand"
