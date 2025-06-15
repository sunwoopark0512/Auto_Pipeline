import builtins
from unittest.mock import MagicMock, patch

import pytest

import google_ads_cpc


def test_fetch_cpc_returns_value_and_uses_client(monkeypatch):
    google_ads_cpc.fetch_cpc.cache_clear()
    mock_row = MagicMock()
    mock_row.metrics.average_cpc.micros = 2500000

    service_mock = MagicMock()
    service_mock.search.return_value = [mock_row]

    client_mock = MagicMock()
    client_mock.get_service.return_value = service_mock

    with patch('google_ads_cpc.GoogleAdsClient') as client_cls:
        client_cls.load_from_dict.return_value = client_mock
        monkeypatch.setenv('GOOGLE_ADS_DEVELOPER_TOKEN', 'token')
        monkeypatch.setenv('GOOGLE_ADS_CLIENT_ID', 'cid')
        monkeypatch.setenv('GOOGLE_ADS_CLIENT_SECRET', 'secret')
        monkeypatch.setenv('GOOGLE_ADS_REFRESH_TOKEN', 'refresh')
        monkeypatch.setenv('GOOGLE_ADS_CUSTOMER_ID', '123')
        result = google_ads_cpc.fetch_cpc('test')

    assert result == 2.5
    service_mock.search.assert_called_once()
    client_cls.load_from_dict.assert_called_once()
