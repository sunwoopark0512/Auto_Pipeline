import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import keyword_auto_pipeline as kap
from unittest.mock import patch


def test_fetch_cpc_caching():
    kap.cpc_cache.clear()
    with patch.dict(kap.__dict__, {"CPC_API_USER": "u", "CPC_API_PASSWORD": "p"}):
        with patch('keyword_auto_pipeline.requests.post') as mock_post:
            mock_resp = mock_post.return_value
            mock_resp.json.return_value = {
                'tasks': [{'result': [{'items': [{'cpc': 1200}]}]}]
            }
            mock_resp.raise_for_status.return_value = None
            value1 = kap.fetch_cpc('kw')
            value2 = kap.fetch_cpc('kw')
            assert value1 == 1200
            assert value2 == 1200
            assert mock_post.call_count == 1
