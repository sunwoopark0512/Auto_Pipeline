from unittest import mock

import keyword_auto_pipeline as kap


def test_collect_data_instantiates_trendreq():
    with mock.patch.object(kap, 'TrendReq') as mock_trend, \
         mock.patch.object(kap, 'fetch_google_trends', return_value={'source': 'g'}), \
         mock.patch.object(kap, 'fetch_twitter_metrics', return_value={'source': 't'}):
        result = kap.collect_data_for_keyword('kw')
        assert mock_trend.call_count == 1
        assert result == [{'source': 'g'}, {'source': 't'}]


def test_run_pipeline_uses_collect_data(monkeypatch):
    calls = []

    def fake_collect(keyword):
        calls.append(keyword)
        return []

    monkeypatch.setattr(kap, 'collect_data_for_keyword', fake_collect)
    monkeypatch.setattr(kap, 'filter_keywords', lambda entries: [])
    monkeypatch.setattr(kap, 'generate_keyword_pairs', lambda details: ['a', 'b'])
    monkeypatch.setattr(kap, 'log_memory_usage', lambda prefix='': None)

    kap.run_pipeline()
    assert calls == ['a', 'b']


